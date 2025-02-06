from rest_framework import serializers
from ..models import Task
from ..permissions import is_at_least

class TaskReadSerializer(serializers.ModelSerializer):
    """Serializer for listing tasks"""

    owner = serializers.StringRelatedField()

    class Meta:
        model = Task
        fields = ["id", "title", "description", "status", "due_date", "created_at", "updated_at", "owner"]
        read_only_fields = ["id", "created_at", "updated_at", "owner"]

class TaskSerializer(serializers.ModelSerializer):
    """Serializer for creating a new task"""

    class Meta:
        model = Task
        fields = ["id", "title", "description", "status", "due_date", "created_at", "updated_at", "owner"]
        read_only_fields = ["id", "created_at", "updated_at"]
