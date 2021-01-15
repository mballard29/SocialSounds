from rest_framework.permissions import BasePermission

# checks if user is an admin/superuser
class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if user.is_superuser:
            return True
        return False
