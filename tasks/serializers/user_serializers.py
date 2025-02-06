from django.contrib.auth.models import User, Group
from rest_framework import serializers

class UserDetailSerializer(serializers.ModelSerializer):
    """Serializer for retrieving user details"""

    groups = serializers.SlugRelatedField(
        many=True, slug_field="name", read_only=True
    )

    class Meta:
        model = User
        fields = ["id", "username", "email", "groups", "date_joined", "last_login"]
        read_only_fields = ["id", "username", "email", "date_joined", "last_login"]

class AdminUserCreateSerializer(serializers.ModelSerializer):
    """Serializer for Admins to create users with specific roles"""

    password = serializers.CharField(write_only=True, required=True)
    groups = serializers.SlugRelatedField(
        many=True, slug_field="name", queryset=Group.objects.all(), required=False
    )

    class Meta:
        model = User
        fields = ["id", "username", "password", "groups"]

    def create(self, validated_data):
        """Create a new user and assign specified groups"""
        groups = validated_data.pop("groups", [])
        user = User.objects.create_user(**validated_data)
        
        for group in groups:
            user.groups.add(group)
        
        return user