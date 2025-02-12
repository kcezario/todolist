from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

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

class TodoListTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom JWT Serializer for TodoList"""

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = {
            "id": self.user.id,
            "username": self.user.username
        }
        return data