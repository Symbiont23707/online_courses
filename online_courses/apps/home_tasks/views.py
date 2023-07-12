from django.shortcuts import render
from rest_framework import status, generics
from django.core import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.home_tasks.models import Home_task, HomeTaskResult
from apps.home_tasks.serializers import Home_taskSerializer, HomeTaskResultSerializer
from apps.users.models import Student


# Create your views here.

class Home_taskAPIView(generics.ListCreateAPIView):
    # If the course is his course
    queryset = Home_task.objects.all()
    serializer_class = Home_taskSerializer

class HomeTaskResultAPIView(generics.ListCreateAPIView):
    queryset = HomeTaskResult.objects.all()
    serializer_class = HomeTaskResultSerializer

