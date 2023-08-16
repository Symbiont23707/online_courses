from rest_framework import serializers
from libs.types import RoleTypes
from .models import User, Student, Teacher
from ..confirmations.serializers import AccountConfirmationSerializer


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
        user.is_active = False
        user.save()

        confirmation_serializer = AccountConfirmationSerializer(data={'user': user.uuid})
        if confirmation_serializer.is_valid():
            confirmation_serializer.save()

        roles_map = {
            RoleTypes.Student: (Student, {'user': user, 'specialty': specialty}),
            RoleTypes.Teacher: (Teacher, {'user': user}),
        }
        model, kwargs = roles_map[role]
        model.objects.create(**kwargs)

        return user
