from django.core.mail import send_mail
from rest_framework import serializers
from config import settings
from libs.types import MessageConfirmation
from .models import AccountConfirmation


class AccountConfirmationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountConfirmation
        fields = ['uuid', 'expiry_date', 'user']

    def create(self, validated_data):
        confirmation = super().create(validated_data)
        confirmation.save()

        subject = MessageConfirmation.subject

        message = f"Hello,\n\nPlease click on the following link to activate your account:\n"
        message += f"http://{settings.DOMAIN}/api/v1/users/activate/{confirmation.uuid}"

        send_mail(subject, message, settings.EMAIL_HOST_USER, [validated_data['user'].email],
                  fail_silently=False)

        return confirmation
