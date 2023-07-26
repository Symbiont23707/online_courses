import arrow
from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework import serializers

from libs.types import Weekdays, Intervals
from .models import Lecture
from ..courses.models import Course
from ..errors import ErrorMessage


class Schedule(serializers.Serializer):
    interval = serializers.ChoiceField(choices=Intervals)
    weekday = serializers.CharField(max_length=12)
    day = serializers.IntegerField(
        validators=[MaxValueValidator(31), MinValueValidator(1)]
    )
    hour = serializers.IntegerField(
        validators=[MaxValueValidator(23), MinValueValidator(0)]
    )
    minute = serializers.IntegerField(
        validators=[MaxValueValidator(59), MinValueValidator(0)]
    )
    active = serializers.BaseSerializer()


class LectureSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.name', read_only=True)
    schedule = Schedule()

    class Meta:
        model = Lecture
        fields = ['topic', 'presentation', 'course_name', 'course', 'schedule']
        extra_kwargs = {
            'course': {'write_only': True},
        }
        read_only_fields = ['course_name']

    def validate(self, attrs):
        course = attrs['course']

        if not Course.objects.filter(uuid=course.uuid, teachers__user=self.context['request'].user).exists():
            raise serializers.ValidationError(ErrorMessage.PER001.value)

        return attrs

