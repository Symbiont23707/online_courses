from django.shortcuts import render
from rest_framework import viewsets

from apps.lectures.models import Lecture
from apps.lectures.serializers import LectureSerializer


class LectureViewSet(viewsets.ModelViewSet):
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer

    def get_queryset(self):
        if self.request.data['course'] is None:
            return super().get_queryset()
        else:
            return super().get_queryset().filter(course=self.request.data['course'])