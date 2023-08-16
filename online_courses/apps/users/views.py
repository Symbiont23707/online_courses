from django.http import HttpResponse
from rest_framework import generics
from rest_framework.decorators import api_view
from libs.types import MessageConfirmation
from .serializers import UserSerializer
from ..confirmations.models import AccountConfirmation


class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer


@api_view(['GET'])
def activate(request, uuid):
    confirmation = AccountConfirmation.objects.filter(uuid=uuid).first()

    if confirmation.is_expired():
        confirmation.user.is_active = True
        confirmation.user.save()
        confirmation.delete()
        return HttpResponse(MessageConfirmation.accepted_confirmation)
    else:
        return HttpResponse(MessageConfirmation.invalid_link)
