import arrow as arrow
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from apps.courses.models import Course
from libs.abstract_models import BaseUUIDModel


class Lecture(BaseUUIDModel):
    topic = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    presentation = models.FileField(upload_to='media')
    schedule = models.JSONField()
