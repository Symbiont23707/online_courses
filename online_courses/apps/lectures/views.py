from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from apps.courses.permissions import IsTeacherOrReadOnly
from apps.lectures.models import Lecture, Schedule
from apps.lectures.serializers import LectureSerializer, ScheduleSerializer


class LectureAPIView(generics.ListCreateAPIView):
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['topic']

    def get_queryset(self):
        return super().get_queryset().filter(
            Q(course__students__user=self.request.user)
            | Q(course__teachers__user=self.request.user)
        )


class LectureDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer
    lookup_field = 'uuid'
    permission_classes = (IsTeacherOrReadOnly,)

    def get_queryset(self):
        return super().get_queryset().filter(
            Q(course__students__user=self.request.user)
            | Q(course__teachers__user=self.request.user)
        )


class LectureByCourseAPIView(generics.ListAPIView):
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer
    permission_classes = ()

    def get_queryset(self):
        return super().get_queryset().filter(Q(course=self.kwargs['uuid'])
                                             & (Q(course__students__user=self.request.user)
                                                | Q(course__teachers__user=self.request.user))
                                             )


class ScheduleAPIView(generics.ListCreateAPIView):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = ()


class ScheduleDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    lookup_field = 'uuid'
