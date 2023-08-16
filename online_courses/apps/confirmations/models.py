from datetime import timedelta
from django.db import models
from django.utils import timezone
from apps.users.models import User
from libs.abstract_models import BaseUUIDModel


class AccountConfirmation(BaseUUIDModel):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    expiry_date = models.DateTimeField(default=timezone.now() + timedelta(hours=4))

    def is_expired(self):
        return timezone.now() + timedelta(hours=3) < self.expiry_date
