import uuid as uuid
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
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

    class Meta:
        abstract = True

class User(AbstractUser, BaseModel):

    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []