from django.db import models

from apps.home_tasks.models import IntermediateCompletedHome_taskStudent
from apps.users.models import BaseUUIDModel


# Create your models here.
class Mark(BaseUUIDModel):
    MARK_TYPES = (
        ('done', 'Done'),
        ('not done', 'Not done'),
        ('not provided', 'Not provided'),
        ('overdue', 'Overdue')
    )
    rating = models.CharField(choices=MARK_TYPES, max_length=12)
    completed_home_task = models.OneToOneField(IntermediateCompletedHome_taskStudent, on_delete=models.PROTECT, null=True)
    def __str__(self):
        return str(self.uuid)
class Comment(BaseUUIDModel):
    mark = models.ForeignKey(Mark, on_delete=models.PROTECT, null=True)
    comment = models.CharField(max_length=200, null=True)
