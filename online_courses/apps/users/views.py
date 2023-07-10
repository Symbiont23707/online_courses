from django.shortcuts import render
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
import jwt, datetime
import logging

from .models import User
from .serializers import UserSerializer
from ..students.serializers import StudentSerializer
from ..teachers.serializers import TeacherSerializer


# Create your views here.
class RegisterView(APIView):
    """
    Registration a new user in system
    """
    #field specialty
    serializer_class = UserSerializer
    def post(self, request):
        role = request.data.get('role')
        specialty = request.data.get('specialty')

        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        if role == 'Student':
            student_data = {'user': user.uuid, 'specialty': specialty}
            serializer_student = StudentSerializer(data=student_data)
            serializer_student.is_valid(raise_exception=True)
            serializer_student.save()
        else:
            teacher_data = {'user': user.uuid}
            serializer_teacher = TeacherSerializer(data=teacher_data)
            serializer_teacher.is_valid(raise_exception=True)
            serializer_teacher.save()

        return Response(serializer.data)
