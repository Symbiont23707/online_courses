from django.db import models
from apps.users.models import User, BaseUUIDModel


# Create your models here.
class Teacher(BaseUUIDModel):
    user = models.OneToOneField(User, on_delete=models.PROTECT, null=True)
    # object = models.CharField(max_length=50, null=True)

