from rest_framework import serializers
from .models import Home_task, IntermediateCompletedHome_taskStudent
from ..students.models import Student


class HomeTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Home_task
        fields = '__all__'

class IntermediateCompletedHome_taskStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntermediateCompletedHome_taskStudent
        fields = '__all__'

