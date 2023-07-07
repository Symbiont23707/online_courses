from django.db import models

from apps.lectures.models import Lecture
from apps.students.models import Student
from apps.users.models import BaseUUIDModel


# Create your models here.

class Home_task(BaseUUIDModel):
    description = models.TextField(max_length=1000)
    lectures = models.OneToOneField(Lecture, on_delete=models.PROTECT, null=True)
    students = models.ManyToManyField(Student, through='IntermediateCompletedHome_taskStudent')

    def __str__(self):
        return self.uuid


class IntermediateCompletedHome_taskStudent(BaseUUIDModel):
    home_task = models.ForeignKey(Home_task, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    answer = models.CharField(max_length=1000, default='')

    def __str__(self):
        return self.uuid
