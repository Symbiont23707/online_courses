from django.http import HttpResponse, HttpRequest
from django.shortcuts import render

# Create your views here.
from rest_framework import generics, viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Course, IntermediateCourseTeacher, IntermediateCourseStudent
from .serializers import CourseSerializer, IntermediateCourseTeacherSerializer, IntermediateCourseStudentSerializer
from ..students.models import Student
from ..teachers.models import Teacher


# Create your views here.
class CourseViewSet(viewsets.ModelViewSet):
    """
    CRUD courses by teachers
    get(retrieve) for students
    """
    # If the course is his course
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def create(self, request, *args, **kwargs):
        serializer_course = CourseSerializer(data=request.data)
        serializer_course.is_valid(raise_exception=True)
        course = serializer_course.save()

        teacher = Teacher.objects.get(user=request.user)
        teacher_course = IntermediateCourseTeacher.objects.create(course=course, teacher=teacher)
        teacher_course.save()

        return Response(serializer_course.data)

    def get_queryset(self):
        try:
            if self.request.user.student:
                student_uuid = Student.objects.get(user=self.request.user).uuid
                return super().get_queryset().filter(students=student_uuid)
        except Student.DoesNotExist:
            pass

        try:
            teacher_uuid = Teacher.objects.get(user=self.request.user).uuid
            return super().get_queryset().filter(teachers=teacher_uuid)
        except Teacher.DoesNotExist:
            pass



class AddTeacher(APIView):
    """
    Adding a new teacher to his course
    """
    # If the course is his course
    def post(self, request):
        serializer = IntermediateCourseTeacherSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class AddDeleteStudent(APIView):
    """
    Adding/Deleting a Student to his Course
    """
    # If the course is his course
    def post(self, request):
        serializer = IntermediateCourseStudentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request):
        try:
            student = Student.objects.get(uuid=request.data['student'])
            course = Course.objects.get(uuid=request.data['course'])
            obj = IntermediateCourseStudent.objects.filter(student=student, course=course).first()
        except IntermediateCourseStudent.DoesNotExist:
            msg = {'msg': 'not found'}
            return Response(msg, status=status.HTTP_404_NOT_FOUND)
        obj.delete()
        return Response({'msg': 'deleted'}, status=status.HTTP_204_NO_CONTENT)
