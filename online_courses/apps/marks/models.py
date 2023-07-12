from django.db import models

from apps.home_tasks.models import HomeTaskResult
from libs.abstract_models import BaseUUIDModel
from libs.types import MARK_TYPES


class Mark(BaseUUIDModel):
    rating = models.CharField(choices=MARK_TYPES, max_length=12)
    home_task_result = models.OneToOneField(HomeTaskResult, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.uuid)

class Comment(BaseUUIDModel):
    mark = models.ForeignKey(Mark, on_delete=models.PROTECT)
    comment = models.CharField(max_length=200, null=True)
    created_by = models.CharField(max_length=36)

