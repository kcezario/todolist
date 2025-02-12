from django.contrib.auth.models import User, Group
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from ..serializers import RegisterSerializer, UserDetailSerializer, AdminUserCreateSerializer, TodoListTokenObtainPairSerializer
from ..utils import is_at_least

class UserViewSet(viewsets.ModelViewSet):
    """User API with dynamic serializers, permissions, and filters"""
    
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'put', 'delete']
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['username', 'email']
    search_fields = ['username', 'email']
    ordering_fields = ['id', 'username']
    
    def get_queryset(self):
        """Return different queryset based on user permissions"""
        if is_at_least(self.request.user, "Manager"):
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)

    def get_serializer_class(self):
        """Use different serializers based on action"""
        if self.action == "create":
            return AdminUserCreateSerializer
        return UserDetailSerializer


@extend_schema(
    request=RegisterSerializer,
    responses={201: UserDetailSerializer, 400: {"error": "Invalid data"}}
)
@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    """Endpoint to register a new user and assign to 'User' group"""
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    
    group, _ = Group.objects.get_or_create(name="User")
    user.groups.add(group)
    
    return Response(serializer.data, status=status.HTTP_201_CREATED)
    
@extend_schema(
    responses={200: UserDetailSerializer, 401: {"detail": "Authentication credentials were not provided."}}
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    """Endpoint to return details of the authenticated user"""
    serializer = UserDetailSerializer(request.user)
    return Response(serializer.data)
