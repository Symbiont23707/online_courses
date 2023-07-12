from django.db.models import Q
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render

# Create your views here.
from rest_framework import generics, viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Course
from .serializers import CourseSerializer, TeacherCourseSerializer
from ..users.models import Teacher, Student

class CourseAPIView(generics.ListCreateAPIView):
    # If the course is his course
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_queryset(self):
        return super().get_queryset().filter(
            Q(students__user=self.request.user)
            | Q(teachers__user=self.request.user)
        )


class CourseDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_field = 'uuid'

class TeacherAPIView(generics.CreateAPIView):
    # If the course is his course
    serializer_class = TeacherCourseSerializer

