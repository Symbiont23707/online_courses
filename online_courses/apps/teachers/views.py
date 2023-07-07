from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response


# Create your views here.
# class TeacherCourseViewSet(viewsets.ModelViewSet):
#     queryset = TeacherCourse.objects.all()
#     serializer_class = TeacherCourseSerializer
#
#     def create(self, request, *args, **kwargs):
#         # if teacher_uuid in teacher_course
#         serializer_teacher_course = TeacherCourseSerializer(data=request.data)
#         serializer_teacher_course.is_valid(raise_exception=True)
#         serializer_teacher_course.save()
#
#         return Response(serializer_teacher_course.data)
#
#     # def get_queryset(self):
#     #     return super().get_queryset().filter(uuid=self.request.user.uuid)
