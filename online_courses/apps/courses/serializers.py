from rest_framework import serializers, status
from rest_framework.response import Response

from .models import Course
from ..lectures.models import Lecture
from ..lectures.serializers import LectureSerializer
from ..users.models import Teacher


class CourseSerializer(serializers.ModelSerializer):
    # if him posts
    class Meta:
        model = Course
        fields = ['uuid', 'name', 'specialty', 'teachers', 'students']

    def create(self, validated_data):
        teachers_data = validated_data.pop('teachers', None)
        students_data = validated_data.pop('students', None)
        course = super().create(validated_data)

        for teacher in teachers_data:
            course.teachers.add(teacher)
        for student in students_data:
            course.students.add(student)

        return course


class TeacherCourseSerializer(serializers.ModelSerializer):
    uuid = serializers.ChoiceField(choices=Course.objects.all().values_list('uuid', 'uuid'), required=True)
    class Meta:
        model = Course
        fields = ('uuid', 'teachers')

    def create(self, validated_data):
        uuid = validated_data['uuid']
        teachers_data = validated_data.pop('teachers', None)
        course = Course.objects.get(uuid=uuid)
        for teacher in teachers_data:
            course.teachers.add(teacher)
        return course