from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from apps.courses.permissions import IsTeacherOrReadOnly, IsStudentOrReadOnly
from apps.home_tasks.models import HomeTaskResult, HomeTask
from apps.home_tasks.serializers import HomeTaskSerializer, HomeTaskResultSerializer


class HomeTaskAPIView(generics.ListCreateAPIView):
    queryset = HomeTask.objects.all()
    serializer_class = HomeTaskSerializer
    permission_classes = [IsTeacherOrReadOnly | IsAdminUser]
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        return super().get_queryset().filter(
            Q(lectures__course__students__user=self.request.user)
            | Q(lectures__course__teachers__user=self.request.user)
        ).select_related('lectures')


class HomeTaskDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HomeTask.objects.all()
    serializer_class = HomeTaskSerializer
    lookup_field = 'uuid'
    permission_classes = (IsTeacherOrReadOnly, IsAdminUser)

    def get_queryset(self):
        return super().get_queryset().filter(
            Q(lectures__course__students__user=self.request.user)
            | Q(lectures__course__teachers__user=self.request.user)
        )


class HomeTaskResultAPIView(generics.ListCreateAPIView):
    queryset = HomeTaskResult.objects.all()
    serializer_class = HomeTaskResultSerializer
    permission_classes = (IsStudentOrReadOnly, IsAdminUser)

    def get_queryset(self):
        return super().get_queryset().filter(
            Q(home_task__lectures__course__students__user=self.request.user)
            | Q(home_task__lectures__course__teachers__user=self.request.user)
        ).select_related('home_task')


class HomeTaskResultDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HomeTaskResult.objects.all()
    serializer_class = HomeTaskResultSerializer
    lookup_field = 'uuid'
    permission_classes = (IsStudentOrReadOnly, IsAdminUser)

    def get_queryset(self):
        return super().get_queryset().filter(
            Q(home_task__lectures__course__students__user=self.request.user)
            | Q(home_task__lectures__course__teachers__user=self.request.user)
        )
