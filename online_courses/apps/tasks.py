from celery import shared_task
from django.db.models import Q
from apps.lectures.models import Lecture
import arrow
from apps.websocket_utils import push_lecture_notification
from apps.zoom.views import ZoomAPIClient
from libs.types import Intervals, StatusLecture, MessageEmail, WS


@shared_task
def send_lecture_notifications():
    now = arrow.utcnow().shift(hours=+4)
    lectures_to_notify = Lecture.objects.filter(Q(schedule__hour=int(now.format('H')),
                                                  schedule__minute=int(now.format('m')),
                                                  schedule__active=StatusLecture.active)
                                                & (Q(schedule__interval=Intervals.day)
                                                   |
                                                   Q(schedule__interval=Intervals.week,
                                                     schedule__weekday=now.format('dddd'))
                                                   |
                                                   Q(schedule__interval=Intervals.month,
                                                     schedule__day=now.format('d')))
                                                )

    for lecture in lectures_to_notify:
        subject = lecture.topic
        start_time = arrow.utcnow().shift(hours=+4).format("YYYY-MM-DD")
        join_url = ZoomAPIClient.create_zoom_meeting(topic=subject, start_time=start_time, lecture=lecture)
        message = MessageEmail.message + str(now)[11:20] + '\n' + MessageEmail.link + join_url
        push_lecture_notification(lecture.uuid,
                                  {'subject': subject, 'message': message,
                                   'recipient_list': [student.user.email for student in lecture.course.students.all()],
                                   'type': WS.WS_LECTURE_NOTIFICATIONS})
