from celery import shared_task
from django.db.models import Q
from apps.lectures.models import Lecture
import arrow
from apps.websocket_utils import push_lecture_notification
from apps.zoom.models import Meeting
from apps.zoom.zoom_client import ZoomAPIClient
from config import settings
from libs import zoom_configuration
from libs.types import Intervals, StatusLecture, MessageEmail, WS


@shared_task
def send_lecture_notifications():
    client_zoom = ZoomAPIClient(
        zoom_secret_token=settings.ZOOM_SECRET_TOKEN,
        zoom_client_id=settings.ZOOM_CLIENT_ID,
        zoom_account_id=settings.ZOOM_ACCOUNT_ID,
        zoom_client_secret=settings.ZOOM_CLIENT_SECRET
    )
    now = arrow.utcnow().shift(hours=+4)
    lectures_to_notify = Lecture.objects.filter(
        Q(schedule__hour=int(now.format('H')),
          schedule__minute=int(now.format('m')),
          schedule__active=StatusLecture.active)

        & (
           Q(schedule__interval=Intervals.day)
           |
           Q(schedule__interval=Intervals.week,
             schedule__weekday=now.format('dddd'))
           |
           Q(schedule__interval=Intervals.month,
             schedule__day=now.format('d'))
           )
        )

    for lecture in lectures_to_notify:
        subject = lecture.topic
        start_time = arrow.utcnow().shift(hours=+4).format("YYYY-MM-DD")
        meeting_data = client_zoom.create_zoom_meeting(
            topic=subject,
            start_time=start_time,
            data=zoom_configuration.data,
            content_type='application/json'
        )

        Meeting.objects.create(
            uuid=meeting_data['uuid'], meeting_id=int(meeting_data['id']),
            host_email=meeting_data['host_email'], duration=int(meeting_data['duration']),
            topic=meeting_data['topic'], lecture=lecture, participants_count=0
        )

        message = MessageEmail.message + str(now)[11:20] + '\n' + MessageEmail.link + meeting_data['join_url']

        push_lecture_notification(lecture.uuid,
                                  {'subject': subject, 'message': message,
                                   'recipient_list': [student.user.email for student in lecture.course.students.all()],
                                   'type': WS.WS_LECTURE_NOTIFICATIONS})
