from rest_framework import generics
from .serializers import UserSerializer

class RegisterView(generics.CreateAPIView):
    """
    Registration a new user in system
    """
    serializer_class = UserSerializer

