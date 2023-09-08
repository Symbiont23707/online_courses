import uuid as uuid
from django.db import models


class BaseUUIDModel(models.Model):
    """Abstract base model that implements `uuid` field."""

    uuid = models.UUIDField(
        verbose_name=("uuid"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return str(self.uuid)


class BaseModel(BaseUUIDModel):
    """
    Abstract base model that implements fields:
        - uuid
        - created_at
        - updated_at
    """

    created_at = models.DateTimeField(
        verbose_name=("Created at"),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name=("Updated at"),
        auto_now=True,
    )

    invited_by = models.CharField(
        default='',
        max_length=200,
        verbose_name=('Invited by')
    )

    class Meta:
        abstract = True
