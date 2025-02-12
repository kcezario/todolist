from rest_framework import serializers
from ..models import Task

class TaskReadSerializer(serializers.ModelSerializer):
    """Serializer for listing tasks"""

    owner = serializers.StringRelatedField()

    class Meta:
        model = Task
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at", "owner"]

class TaskSerializer(serializers.ModelSerializer):
    """Serializer for creating a new task"""

    class Meta:
        model = Task
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at", "owner"]
