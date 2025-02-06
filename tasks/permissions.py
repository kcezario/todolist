from rest_framework.permissions import BasePermission
from tasks.utils import is_at_least

class IsAdmin(BasePermission):
    """Admins can do anything"""

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and is_at_least(request.user, "Admin")

class IsManagerOrOwner(BasePermission):
    """
    Managers can list all tasks but can only modify their own.
    Regular users can only modify their own tasks.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if is_at_least(request.user, "Admin"):
            return True
        if is_at_least(request.user, "Manager"):
            return (
                request.method in ["GET", "POST", "PUT", "DELETE"]
                and obj.owner == request.user
            )
        return obj.owner == request.user
