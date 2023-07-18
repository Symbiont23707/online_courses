from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from apps.courses.permissions import IsTeacherOrReadOnly, IsStudentOrReadOnly
from apps.home_tasks.models import Home_task, HomeTaskResult
from apps.home_tasks.serializers import Home_taskSerializer, HomeTaskResultSerializer


class Home_taskAPIView(generics.ListCreateAPIView):
    queryset = Home_task.objects.all()
    serializer_class = Home_taskSerializer
    permission_classes = (IsTeacherOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    ordering_fields = ['rating']

    def get_queryset(self):
        return super().get_queryset().filter(
            Q(lectures__course__students__user=self.request.user)
            | Q(lectures__course__teachers__user=self.request.user)
        ).select_related('lectures')


class Home_taskDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Home_task.objects.all()
    serializer_class = Home_taskSerializer
    lookup_field = 'uuid'
    permission_classes = (IsTeacherOrReadOnly,)

    def get_queryset(self):
        return super().get_queryset().filter(
            Q(lectures__course__students__user=self.request.user)
            | Q(lectures__course__teachers__user=self.request.user)
        )


class HomeTaskResultAPIView(generics.ListCreateAPIView):
    queryset = HomeTaskResult.objects.all()
    serializer_class = HomeTaskResultSerializer
    permission_classes = (IsStudentOrReadOnly,)

    def get_queryset(self):
        return super().get_queryset().filter(
            Q(home_tasks__lectures__course__students__user=self.request.user)
            | Q(home_tasks__lectures__course__teachers__user=self.request.user)
        ).select_related('home_tasks')


class HomeTaskResultDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HomeTaskResult.objects.all()
    serializer_class = HomeTaskResultSerializer
    lookup_field = 'uuid'
    permission_classes = (IsStudentOrReadOnly,)

    def get_queryset(self):
        return super().get_queryset().filter(
            Q(home_tasks__lectures__course__students__user=self.request.user)
            | Q(home_tasks__lectures__course__teachers__user=self.request.user)
        )
