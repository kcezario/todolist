from rest_framework import viewsets
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Task
from ..serializers import TaskSerializer, TaskReadSerializer
from ..filters import TaskFilter
from ..utils import is_at_least


class TaskViewSet(viewsets.ModelViewSet):
    """Task API with filtering and permissions"""

    queryset = Task.objects.all().order_by("id")
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = TaskFilter
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title', 'description']
    filterset_fields = ['status', 'due_date', 'owner']

    def get_serializer_class(self):
        """Use different serializers for different actions"""
        if self.action in ["list", "retrieve"]:
            return TaskReadSerializer
        return TaskSerializer

    def get_queryset(self):
        """Return different task lists based on user permissions"""
        queryset = Task.objects.all() if is_at_least(self.request.user, "Manager") else Task.objects.filter(owner=self.request.user)
        return queryset

    @extend_schema(
        summary="List all tasks",
        parameters=[
            OpenApiParameter(name="search", description="Search by title or description", required=False, type=str),
            OpenApiParameter(name="status", description="Filter by status", required=False, type=str),
            OpenApiParameter(name="due_date", description="Filter by due date", required=False, type=str),
            OpenApiParameter(name="owner", description="Filter by owner ID", required=False, type=int),
        ],
        responses={200: TaskReadSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        """List all tasks (Admin/Manager sees all, Users see only their own)"""
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Retrieve a specific task",
        responses={200: TaskReadSerializer, 404: {"detail": "Not found"}}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Create a new task",
        request=TaskSerializer,
        responses={201: TaskReadSerializer, 400: {"detail": "Invalid data"}}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Update a task",
        request=TaskSerializer,
        responses={200: TaskReadSerializer, 403: {"detail": "Not authorized"}, 404: {"detail": "Not found"}}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Partially update a task",
        request=TaskSerializer(partial=True),
        responses={200: TaskReadSerializer, 403: {"detail": "Not authorized"}, 404: {"detail": "Not found"}}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete a task",
        responses={204: None, 403: {"detail": "Not authorized"}, 404: {"detail": "Not found"}}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
