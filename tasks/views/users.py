# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework import status
# from django.contrib.auth.models import User, Group
# from ..serializers import UserSerializer
# from ..utils.is_at_least import is_at_least
# from drf_spectacular.utils import extend_schema, OpenApiExample

# @extend_schema(
#     summary="Admin-only endpoint to create users and assign roles",
#     request=UserSerializer,
#     responses={
#         201: UserSerializer,
#         400: OpenApiExample(
#             name="User already exists",
#             value={"error": "User with this username already exists."},
#             response_only=True
#         ),
#         403: OpenApiExample(
#             name="Permission denied",
#             value={"detail": "You do not have permission to perform this action."},
#             response_only=True
#         )
#     }
# )
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def create_user(request):
#     """Admin-only endpoint to create users and assign roles"""
#     if not is_at_least(request.user, "Admin"):
#         return Response({"detail": "You do not have permission to perform this action."}, status=403)

#     serializer = UserSerializer(data=request.data)
#     if serializer.is_valid():
#         user = serializer.save()

#         group_name = request.data.get("group", None)
#         if group_name:
#             group, _ = Group.objects.get_or_create(name=group_name)
#             user.groups.add(group)

#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
