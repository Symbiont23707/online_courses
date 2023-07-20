from rest_framework import serializers
from .models import Lecture
from ..courses.models import Course
from ..errors import ErrorMessage


class LectureSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.name', read_only=True)

    class Meta:
        model = Lecture
        fields = ['topic', 'presentation', 'course_name', 'course']
        extra_kwargs = {'course': {'write_only': True}}
        read_only_fields = ['course_name']

    def validate(self, attrs):
        course = attrs['course']

        if not Course.objects.filter(uuid=course.uuid, teachers__user=self.context['request'].user).exists():
            raise serializers.ValidationError(ErrorMessage.PER001.value)

        return attrs
