from rest_framework.permissions import BasePermission,SAFE_METHODS
from account.models import User
class IsAdmin(BasePermission):
    message = "You must have super admin access"
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_superuser and request.user.role == User.ADMIN

class IsMember(BasePermission):
    message = "You must have member access"
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == User.MEMBER