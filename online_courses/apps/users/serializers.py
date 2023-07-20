from rest_framework import serializers

from libs.types import RoleTypes
from .models import User, Student, Teacher


class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=RoleTypes.choices, write_only=True)
    specialty = serializers.CharField(max_length=50, write_only=True, required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'role', 'specialty']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        role = validated_data.pop('role', None)
        specialty = validated_data.pop('specialty', None)
        user = super().create(validated_data)
        if password is not None:
            user.set_password(password)
        user.save()
        roles_map = {
            RoleTypes.Student: (Student, {'user': user, 'specialty': specialty}),
            RoleTypes.Teacher: (Teacher, {'user': user}),
        }
        model, kwargs = roles_map[role]
        model.objects.create(**kwargs)

        return user
