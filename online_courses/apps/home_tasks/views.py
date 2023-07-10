from django.shortcuts import render
from rest_framework import status
from django.core import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.home_tasks.models import IntermediateCompletedHome_taskStudent, Home_task
from apps.home_tasks.serializers import HomeTaskSerializer, IntermediateCompletedHome_taskStudentSerializer
from apps.students.models import Student


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

        home_task_uuid = request.data.get('home_task')
        answer = request.data.get('answer')
        student_uuid = request.user.student.uuid

        try:
            home_task = Home_task.objects.get(uuid=home_task_uuid)
            student = Student.objects.get(uuid=student_uuid)

            completed_homework = IntermediateCompletedHome_taskStudent(
                home_task=home_task,
                student=student,
                answer=answer
            )
            completed_homework.save()

            return Response(f'U sent answer: {answer} on task number: {home_task.uuid}')

        except Home_task.DoesNotExist:
            return Response({'error': 'Home_task was not found.'}, status=404)

        except Student.DoesNotExist:
            return Response({'error': 'Home_task was not found.'}, status=404)

class MyHomeTasks(APIView):

    def get(self, request):
        student = Student.objects.get(user=request.user.uuid)
        completed_homeworks = student.home_task_set.all()
        serializer = HomeTaskSerializer(completed_homeworks, many=True)
        return Response(serializer.data)
