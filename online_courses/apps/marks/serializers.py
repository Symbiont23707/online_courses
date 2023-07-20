from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from apps.errors import ErrorMessage
from apps.marks.models import Mark, Comment


class MarkSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=CurrentUserDefault())
    class Meta:
        model = Mark
        fields = ['uuid', 'rating', 'home_task_result', 'created_by']
        read_only_fields = ['created_by']

    def validate(self, attrs):
        home_task_result = attrs['home_task_result']

        if not home_task_result.home_task.lectures.course.teachers.filter(user=self.context['request'].user).exists():
            raise serializers.ValidationError(ErrorMessage.PER001.value)

        return attrs


class CommentSerializer(serializers.ModelSerializer):
    mark_rating = serializers.CharField(source='mark.rating', read_only=True)
    created_by = serializers.HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Comment
        fields = ['uuid', 'comment', 'mark_rating', 'created_by', 'mark']
        extra_kwargs = {'mark': {'write_only': True}}
        read_only_fields = ['created_by', 'mark_rating']

    def validate(self, attrs):
        user = self.context['request'].user
        mark = attrs['mark']

        if mark.created_by != user:
            raise serializers.ValidationError(ErrorMessage.PER001.value)

        return attrs
