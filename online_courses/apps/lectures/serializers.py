from rest_framework import serializers
from .models import Lecture


class LectureSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.name', read_only=True)

    class Meta:
        model = Lecture
        fields = ['topic', 'presentation', 'course_name', 'course']
        extra_kwargs = {'course': {'write_only': True}}
        read_only_fields = ['course_name']

