from django.db import models


class ErrorMessage(models.TextChoices):
    PER001 = 'Current teacher does not have permission'
    PER002 = 'Current student does not have permission'
