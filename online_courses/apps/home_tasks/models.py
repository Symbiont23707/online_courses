from django.db import models
from apps.lectures.models import Lecture
from apps.users.models import Student
from libs.abstract_models import BaseUUIDModel


class HomeTask(BaseUUIDModel):
    description = models.TextField(max_length=1000)
    lectures = models.OneToOneField(Lecture, on_delete=models.PROTECT)


class HomeTaskResult(BaseUUIDModel):
    home_task = models.ForeignKey(HomeTask, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    answer = models.CharField(max_length=1000, default='')
