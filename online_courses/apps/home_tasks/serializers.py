from rest_framework import serializers
from .models import Home_task, HomeTaskResult
from ..users.models import Student


class Home_taskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Home_task
        fields = '__all__'

class HomeTaskResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeTaskResult
        fields = ['home_tasks', 'answer']

    def create(self, validated_data):
        validated_data['students'] = Student.objects.get(user=self.context['request'].user.uuid)
        home_task_result = super().create(validated_data)
        return home_task_result
