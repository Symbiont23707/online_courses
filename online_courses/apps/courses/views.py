from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from .models import Course
from .permissions import IsTeacherOrReadOnly
from .serializers import CourseSerializer


class CourseAPIView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (IsTeacherOrReadOnly,)
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['name', 'specialty']
    orderingset_fields = ['name']

    def get_queryset(self):
        return super().get_queryset().filter(
            Q(students__user=self.request.user) | Q(teachers__user=self.request.user)
        )


class CourseDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_field = 'uuid'
    permission_classes = (IsTeacherOrReadOnly,)

    def get_queryset(self):
        return super().get_queryset().filter(
            Q(students__user=self.request.user) | Q(teachers__user=self.request.user))
