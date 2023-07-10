from django.shortcuts import render
from rest_framework import viewsets

from apps.lectures.models import Lecture
from apps.lectures.serializers import LectureSerializer


class LectureViewSet(viewsets.ModelViewSet):
    """
    CRUD lectures of your courses (A lecture is a topic and a file with a presentation)
    """
    # If the course is his course
    # show only his lectures
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer

    def get_queryset(self):
        course_id = self.request.query_params.get('course')
        if course_id is None:
            return super().get_queryset()
        else:
            return super().get_queryset().filter(course=course_id)