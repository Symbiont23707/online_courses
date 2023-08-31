from datetime import timedelta
from django.utils import timezone
from apps.lectures.models import Lecture
from libs.abstract_models import BaseUUIDModel
from django.db import models


class Meeting(BaseUUIDModel):
    uuid = models.CharField(max_length=40)
    meeting_id = models.BigIntegerField()
    host_email = models.EmailField()
    topic = models.CharField(max_length=100)
    start_time = models.DateTimeField(default=timezone.now() + timedelta(hours=4))
    duration = models.IntegerField()
    lecture = models.OneToOneField(Lecture, on_delete=models.PROTECT)
    participants_count = models.IntegerField(default=0)



