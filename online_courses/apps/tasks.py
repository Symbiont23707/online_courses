from celery import shared_task
from django.core.mail import send_mail
from django.db.models import Q

from apps.lectures.models import Lecture
import arrow

from apps.websocket_utils import push_lecture_notification
from config import settings
from libs.types import Intervals, StatusLecture, MessageEmail, WS


def get_lecture_notification(lecture_uuid):
    return f'{WS.WS_LECTURE_NOTIFICATIONS}_{lecture_uuid}'


@shared_task
def send_lecture_notifications():
    # now = arrow.utcnow() #UTC
    now = arrow.now('Europe/Minsk').shift(hours=+1)
    print(now)
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
        message = MessageEmail.message + str(now)[11:20]
        push_lecture_notification(lecture.uuid,
                                  {'subject': subject, 'message': message,
                                   'recipient_list': [student.user.email for student in lecture.course.students.all()],
                                   'type': WS.WS_LECTURE_NOTIFICATIONS})

        # students_to_notify = lecture.course.students.all()
        # recipient_list = []
        # for student in students_to_notify:
        #     recipient_list.append(student.user.email)
        # send_mail(subject, message, email_from, recipient_list, fail_silently=False)
