from django.db import models
from apps.courses.models import Course
from apps.users.models import BaseUUIDModel


# Create your models here.

class Lecture(BaseUUIDModel):
    topic = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.PROTECT, null=True)
    presentation = models.FileField(upload_to='pdf')

