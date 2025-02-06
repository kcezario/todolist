from django.contrib.auth.models import User, Group
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from ..serializers import RegisterSerializer, UserLoginSerializer, UserDetailSerializer, AdminUserCreateSerializer
from ..utils import is_at_least

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
    request=UserLoginSerializer,
    responses={200: {"token": "string"}, 400: {"error": "Invalid credentials"}}
)
@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    """Endpoint to authenticate user and return token"""
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response(serializer.save(), status=status.HTTP_200_OK)

@extend_schema(
    responses={204: None, 401: {"detail": "Authentication credentials were not provided."}}
)
@api_view(["POST"])
def logout(request):
    """Endpoint to log out and delete the token"""
    if request.auth:
        request.auth.delete()
        return Response(
            {"message": "Logged out successfully"}, status=status.HTTP_204_NO_CONTENT
        )

@extend_schema(
    responses={200: UserDetailSerializer, 401: {"detail": "Authentication credentials were not provided."}}
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    """Endpoint to return details of the authenticated user"""
    serializer = UserDetailSerializer(request.user)
    return Response(serializer.data)

@extend_schema(
    responses={200: UserDetailSerializer(many=True), 403: {"detail": "Not authorized"}}
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def users(request):
    """Endpoint to list all users (only accessible by Admins)"""
    if is_at_least(request.user, "Admin"):
        users = User.objects.all()
        serializer = UserDetailSerializer(users, many=True)
        return Response(serializer.data)
    
    return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

@extend_schema(
    responses={200: UserDetailSerializer, 403: {"detail": "Not authorized"}, 404: {"detail": "User not found"}}
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_detail(request, id):
    """Endpoint to return details of a specific user (only accessible by Managers and above)"""
    if is_at_least(request.user, "Manager"):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserDetailSerializer(user)
        return Response(serializer.data)
    
    return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

@extend_schema(
    request=AdminUserCreateSerializer,
    responses={201: UserDetailSerializer, 400: {"error": "Invalid data"}, 403: {"detail": "Not authorized"}}
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_user(request):
    """Endpoint for Admin to create a new user with specified groups (roles)"""
    if is_at_least(request.user, "Admin"):
        serializer = AdminUserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)



