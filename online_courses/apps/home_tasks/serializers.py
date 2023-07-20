from rest_framework import serializers
from .models import HomeTaskResult, HomeTask
from ..errors import ErrorMessage
from ..fields import CurrentStudentDefault


class HomeTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeTask
        fields = '__all__'

    def validate(self, attrs):
        lectures = attrs['lectures']

        if not lectures.course.teachers.filter(user=self.context['request'].user).exists():
            raise serializers.ValidationError(ErrorMessage.PER001.value)

        return attrs


class HomeTaskResultSerializer(serializers.ModelSerializer):
    student = serializers.HiddenField(default=CurrentStudentDefault())

    class Meta:
        model = HomeTaskResult
        fields = ['uuid', 'home_task', 'answer', 'student']

    def validate(self, attrs):
        home_task = attrs['home_task']

        if not home_task.lectures.course.students.filter(user=self.context['request'].user).exists():
            raise serializers.ValidationError(ErrorMessage.PER002.value)

        return attrs
