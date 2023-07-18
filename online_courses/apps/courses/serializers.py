from rest_framework import serializers, status

from .models import Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['uuid', 'name', 'specialty', 'teachers', 'students']
