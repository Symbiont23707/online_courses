from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from apps.courses.permissions import IsTeacherOrReadOnly, IsStudentOrReadOnly
from apps.marks.models import Mark, Comment
from apps.marks.serializers import MarkSerializer, CommentSerializer


class MarkAPIView(generics.ListCreateAPIView):
    queryset = Mark.objects.all()
    serializer_class = MarkSerializer
    permission_classes = [IsTeacherOrReadOnly | IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    ordering_fields = ['rating']

    def get_queryset(self):
        return super().get_queryset().filter(
            Q(home_task_result__student__user=self.request.user)
            | Q(home_task_result__home_task__lectures__course__teachers__user=self.request.user)
        ).select_related('home_task_result')


class MarkDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Mark.objects.all()
    serializer_class = MarkSerializer
    lookup_field = 'uuid'
    permission_classes = [IsTeacherOrReadOnly | IsAdminUser]

    def get_queryset(self):
        return super().get_queryset().filter(
            Q(home_task_result__student__user=self.request.user)
            | Q(home_task_result__home_task__lectures__course__teachers__user=self.request.user)
        )


class CommentAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsTeacherOrReadOnly | IsStudentOrReadOnly | IsAdminUser]

    def get_queryset(self):
        return super().get_queryset().filter(
            Q(mark__home_task_result__student__user=self.request.user)
            | Q(mark__home_task_result__home_task__lectures__course__teachers__user=self.request.user)
        ).select_related('mark')


class CommentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'uuid'
    permission_classes = [IsTeacherOrReadOnly | IsAdminUser]

    def get_queryset(self):
        return super().get_queryset().filter(
            Q(mark__home_task_result__student__user=self.request.user)
            | Q(mark__home_task_result__home_task__lectures__course__teachers__user=self.request.user)
        )
