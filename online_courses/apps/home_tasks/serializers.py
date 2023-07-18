from rest_framework import serializers
from .models import Home_task, HomeTaskResult
from ..users.models import Student


class Home_taskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Home_task
        fields = '__all__'

    def validate(self, attrs):
        lectures = attrs['lectures']

        if not lectures.course.teachers.filter(user=self.context['request'].user).exists():
            raise serializers.ValidationError("Teacher does not permission to this lecture.")

        return attrs


class HomeTaskResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeTaskResult
        fields = ['uuid', 'home_tasks', 'answer']

    def create(self, validated_data):
        validated_data['students'] = self.context['request'].user.student
        home_task_result = super().create(validated_data)
        return home_task_result

    def validate(self, attrs):
        home_tasks = attrs['home_tasks']

        if not home_tasks.lectures.course.students.filter(user=self.context['request'].user).exists():
            raise serializers.ValidationError("Student does not permission to this home task.")

        return attrs
