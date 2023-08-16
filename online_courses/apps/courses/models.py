from django.db import models
from apps.users.models import Teacher, Student
from libs.abstract_models import BaseUUIDModel


class Course(BaseUUIDModel):
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)
    teachers = models.ManyToManyField(Teacher)
    students = models.ManyToManyField(Student)

    def __str__(self):
        return self.name
