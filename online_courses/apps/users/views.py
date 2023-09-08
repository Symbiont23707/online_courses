from django.http import HttpResponse
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from libs.types import MessageConfirmation
from .serializers import UserSerializer, PasswordResetSerializer, ChangePasswordSerializer, InviteSerializer
from ..confirmations.models import AccountConfirmation


@authentication_classes([])
@permission_classes([])
class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer


@authentication_classes([])
@permission_classes([])
class ResetPasswordView(generics.CreateAPIView):
    serializer_class = PasswordResetSerializer


@authentication_classes([])
@permission_classes([])
class ChangePasswordView(generics.CreateAPIView):
    serializer_class = ChangePasswordSerializer


class InviteView(generics.CreateAPIView):
    serializer_class = InviteSerializer


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def activate(request, activation_uuid):
    confirmation = AccountConfirmation.objects.filter(uuid=activation_uuid).first()

    if confirmation.is_expired():
        confirmation.user.is_active = True
        confirmation.user.save()
        confirmation.delete()
        return HttpResponse(MessageConfirmation.accepted_confirmation)
    else:
        return HttpResponse(MessageConfirmation.invalid_link)
