from rest_framework import serializers
from .models import Course, IntermediateCourseTeacher, IntermediateCourseStudent


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class IntermediateCourseTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntermediateCourseTeacher
        fields = '__all__'

class IntermediateCourseStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntermediateCourseStudent
        fields = '__all__'