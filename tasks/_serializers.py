from django.db import models
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import Task

class UserSerializer(serializers.ModelSerializer):
    """serializer for user registration and authentication"""

    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["id", "username", "password"]

    def create(self, validated_data):
        """Create a new user and hash the password"""
        user = User.objects.create_user(**validated_data)
        return user


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for Admin to create users with roles (groups)"""

    password = serializers.CharField(write_only=True, required=True)
    groups = serializers.SlugRelatedField(
        many=True, slug_field="name", queryset=Group.objects.all()
    )

    class Meta:
        model = User
        fields = ["username", "password", "groups"]

    def create(self, validated_data):
        groups = validated_data.pop("groups", [])
        user = User.objects.create_user(**validated_data)

        for group in groups:
            user.groups.add(group)

        return user


class LoginSerializer(serializers.Serializer):
    """Serializer to validate login data"""

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """Validate user credentials"""
        user = authenticate(username=data["username"], password=data["password"])

        if not user:
            raise serializers.ValidationError({"error": "Invalid credentials"})

        self.context["user"] = user
        return data

    def create(self, validated_data):
        """Return the token for the authenticated user"""
        user = self.context["user"]
        token, _ = Token.objects.get_or_create(user=user)
        return {"token": token.key}
    
    
class TaskSerializer(serializers.ModelSerializer):
    """Serializer for Task model"""
    
    owner = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False
    )

    class Meta:
        model = Task
        fields = '__all__'