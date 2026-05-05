from rest_framework import serializers

from user.models.user import User


class LoginSerializer(serializers.Serializer):
        email = serializers.EmailField()
        password = serializers.CharField(min_length=8, write_only=True)