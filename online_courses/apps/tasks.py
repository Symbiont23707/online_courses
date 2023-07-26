from datetime import datetime, timedelta, time
from celery import shared_task
from django.core.mail import send_mail
from django.db.models import Q

from apps.lectures.models import Lecture, Schedule
import arrow
from config import settings
from libs.types import Weekdays, Intervals

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'sampletextsampletext4@gmail.com'
EMAIL_HOST_PASSWORD = 'Adminadmin2001'
EMAIL_USE_SSL = False


@shared_task
def send_lecture_notifications():
    email_from = settings.EMAIL_HOST_USER
    now = arrow.now('Europe/Minsk').shift(hours=+1)#UTC
    lectures_to_notify = Lecture.objects.filter(Q(schedule__hour=now.format('H'),
                                                  schedule__minute=now.format('m'),
                                                  schedule__status=True)
                                                & (Q(schedule__interval=Intervals.day)
                                                   |
                                                   Q(schedule__interval=Intervals.week,
                                                     schedule__weekday=now.format('dddd'))
                                                   |
                                                   Q(schedule__interval=Intervals.month,
                                                       schedule__weekday=now.format('d')))
                                                )

    for lecture in lectures_to_notify:
        recipient_list = []
        subject = lecture.topic
        message = f'Lecture will be in {now}'#CONSTANT
        students_to_notify = lecture.course.students.all()

        for student in students_to_notify:
            recipient_list.append(student.user.email)
        send_mail(subject, message, email_from, recipient_list)

    return 'hi'
