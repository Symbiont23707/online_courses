from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.shortcuts import get_object_or_404
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import serializers
from config import settings
from libs.types import RoleTypes, MessageUser, UserUrls
from .models import User, Student, Teacher
from ..confirmations.serializers import AccountConfirmationSerializer
from apps.sending_mails.sending_mail import Mail


class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=RoleTypes.choices, write_only=True)
    specialty = serializers.CharField(max_length=50, write_only=True, required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'role', 'specialty']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        role = validated_data.pop('role', None)
        specialty = validated_data.pop('specialty', None)
        user = super().create(validated_data)
        encoded_uuid = self.context.get('request').query_params.get('encoded_uuid')

        if encoded_uuid is not None:
            uid = force_text(urlsafe_base64_decode(encoded_uuid))
            invitation_sender = get_user_model().objects.get(uuid=uid)
            user.invited_by = str(invitation_sender)

        if password is not None:
            user.set_password(password)
        user.is_active = False
        user.save()

        confirmation_serializer = AccountConfirmationSerializer(data={'user': user.uuid})
        if confirmation_serializer.is_valid():
            confirmation_serializer.save()

        roles_map = {
            RoleTypes.Student: (Student, {'user': user, 'specialty': specialty}),
            RoleTypes.Teacher: (Teacher, {'user': user}),
        }
        model, kwargs = roles_map[role]
        model.objects.create(**kwargs)

        return user


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        fields = ['email']

    def create(self, validated_data):
        email = validated_data["email"]

        user = get_object_or_404(User, email=email)

        token = PasswordResetTokenGenerator().make_token(user)
        encoded_uuid = urlsafe_base64_encode(force_bytes(user.uuid))

        params = {'token': token, 'encoded_uuid': encoded_uuid}
        reset_url = f"{UserUrls.base_reset_url}?{'&'.join([f'{key}={value}' for key, value in params.items()])}"

        mail = Mail(
            subject=MessageUser.reset_password,
            message=MessageUser.click_to_reset_link + reset_url,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email]
                    )
        mail.send()

        return validated_data


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, required=True)
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        fields = ['password', 'password_confirm']

    def create(self, validated_data):

        request = self.context.get('request')
        encoded_uuid = request.query_params.get('encoded_uuid')
        token = request.query_params.get('token')

        uid = force_text(urlsafe_base64_decode(encoded_uuid))
        user = get_object_or_404(User, uuid=uid)

        if (user and PasswordResetTokenGenerator().check_token(user, token) and
                (validated_data["password"] == validated_data["password_confirm"])):
            user.set_password(validated_data['password'])
            user.save()

        return encoded_uuid


class InviteSerializer(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        fields = ['email']

    def create(self, validated_data):
        email = validated_data['email']
        user = self.context['request'].user

        encoded_uuid = urlsafe_base64_encode(force_bytes(user.uuid))
        invite_url = UserUrls.base_invite_url + encoded_uuid

        mail = Mail(
            subject=MessageUser.invite_notification,
            message=MessageUser.invite_to_register + invite_url,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email]
        )
        mail.send()

        return validated_data
