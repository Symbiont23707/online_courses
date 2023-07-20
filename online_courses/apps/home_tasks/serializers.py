from rest_framework import serializers
from .models import HomeTaskResult, HomeTask
from ..errors import ErrorMessage
from ..fields import CurrentStudentDefault
from ..lectures.models import Lecture


class HomeTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeTask
        fields = '__all__'

    def validate(self, attrs):
        lectures = attrs['lectures']
        user = self.context['request'].user

        if not Lecture.objects.filter(uuid=lectures.uuid, course__teachers__user=user).exists():
            raise serializers.ValidationError(ErrorMessage.PER001.value)

        return attrs


class HomeTaskResultSerializer(serializers.ModelSerializer):
    student = serializers.HiddenField(default=CurrentStudentDefault())

    class Meta:
        model = HomeTaskResult
        fields = ['uuid', 'home_task', 'answer', 'student']

    def validate(self, attrs):
        home_task = attrs['home_task']
        user = self.context['request'].user

        if not HomeTask.objects.filter(uuid=home_task.uuid, lectures__course__students__user=user).exists():
            raise serializers.ValidationError(ErrorMessage.PER002.value)

        return attrs
