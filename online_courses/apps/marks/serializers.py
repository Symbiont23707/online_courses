from rest_framework import serializers
from apps.marks.models import Mark, Comment


class MarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mark
        fields = ['uuid', 'rating', 'home_task_result', 'created_by']
        read_only_fields = ['created_by']


    def validate(self, attrs):
        home_task_result = attrs['home_task_result']

        if not home_task_result.home_tasks.lectures.course.teachers.filter(user=self.context['request'].user).exists():
            raise serializers.ValidationError("Teacher does not permission to set mark.")

        return attrs

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user.teacher
        comment = super().create(validated_data)
        return comment


class CommentSerializer(serializers.ModelSerializer):
    mark_rating = serializers.CharField(source='mark.rating', read_only=True)

    class Meta:
        model = Comment
        fields = ['uuid', 'comment', 'mark_rating', 'created_by', 'mark']
        extra_kwargs = {'mark': {'write_only': True}}
        read_only_fields = ['created_by', 'mark_rating']

    def validate(self, attrs):
        user = self.context['request'].user
        mark = attrs['mark']

        if mark.created_by != user.teacher:
            raise serializers.ValidationError("Teacher does not permission to set mark.")

        return attrs


    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        comment = super().create(validated_data)
        return comment
