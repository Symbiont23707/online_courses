from django.db import models
from apps.users.models import User, BaseUUIDModel


# Create your models here.

class Student(BaseUUIDModel):
    user = models.OneToOneField(User, on_delete=models.PROTECT, null=True)
    specialty = models.CharField(max_length=100)


