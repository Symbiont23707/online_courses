from django.contrib.auth.models import AbstractUser
from django.db import models
from libs.abstract_models import BaseModel, BaseUUIDModel


class User(AbstractUser, BaseModel):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []


class Teacher(BaseUUIDModel):
    user = models.OneToOneField(User, on_delete=models.PROTECT)


class Student(BaseUUIDModel):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    specialty = models.CharField(max_length=100)
