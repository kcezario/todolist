from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token

class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""

    password = serializers.CharField(write_only=True, required=True)
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "password", "token"]

    def create(self, validated_data):
        """Create user and generate token"""
        user = User.objects.create_user(**validated_data)
        token, _ = Token.objects.get_or_create(user=user)
        return {"id": user.id, "username": user.username, "token": token.key}

    def get_token(self, obj):
        return obj["token"]

class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login authentication"""

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    token = serializers.SerializerMethodField()

    def validate(self, data):
        """Validate user credentials and return token"""
        user = authenticate(username=data["username"], password=data["password"])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        self.context["user"] = user
        return data

    def create(self, validated_data):
        """Return authentication token for the user"""
        user = self.context["user"]
        token, _ = Token.objects.get_or_create(user=user)
        return {"token": token.key}