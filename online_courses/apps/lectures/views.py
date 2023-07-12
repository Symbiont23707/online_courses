from django.db.models import Q
from django.shortcuts import render
from rest_framework import viewsets, generics

from apps.lectures.models import Lecture
from apps.lectures.serializers import LectureSerializer

class LectureAPIView(generics.ListCreateAPIView):
    """
    CRUD lectures of your courses (A lecture is a topic and a file with a presentation)
    """
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer

class LectureDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer
    lookup_field = 'uuid'
