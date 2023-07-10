from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    ROLE_TYPES = (
        ('Teacher', 'teacher'),
        ('Student', 'student')
    )

    role = serializers.ChoiceField(choices=ROLE_TYPES, write_only=True)

    specialty = serializers.CharField(max_length=50, write_only=True)

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
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
