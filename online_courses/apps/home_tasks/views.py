from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.home_tasks.models import IntermediateCompletedHome_taskStudent, Home_task
from apps.home_tasks.serializers import HomeTaskSerializer, IntermediateCompletedHome_taskStudentSerializer


# Create your views here.
class HomeTask(APIView):
    def get(self, request):

        lectures = request.data["lectures"]
        if Home_task.objects.filter(lectures=lectures).exists():

            hometask = Home_task.objects.get(lectures=lectures)
            return Response({
                'Home_task': hometask.description,
            })
        else:
            return Response("Home_task doesn't exists", status=status.HTTP_400_BAD_REQUEST)
    def post(self, request):
        serializer = HomeTaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

class Completed_Home_task(APIView):
    def post(self, request):
        serializer = IntermediateCompletedHome_taskStudentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
