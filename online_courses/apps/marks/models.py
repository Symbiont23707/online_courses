from django.db import models

from apps.home_tasks.models import HomeTaskResult
from apps.users.models import User, Teacher
from libs.abstract_models import BaseUUIDModel
from libs.types import MARK_TYPES


class Mark(BaseUUIDModel):
    rating = models.CharField(choices=MARK_TYPES, max_length=12)
    home_task_result = models.OneToOneField(HomeTaskResult, on_delete=models.PROTECT)
    created_by = models.ForeignKey(Teacher, on_delete=models.CASCADE)


class Comment(BaseUUIDModel):
    mark = models.ForeignKey(Mark, on_delete=models.PROTECT)
    comment = models.CharField(max_length=200, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
