from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    """
    Read-only for all authenticated users, write/delete for admins only.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_authenticated and hasattr(request.user, 'profile') and request.user.profile.role == 'admin'

class IsManagerOrAdmin(BasePermission):
    """
    Read-only for staff, write for managers and admins.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.method in SAFE_METHODS:
            return True
        return hasattr(request.user, 'profile') and request.user.profile.role in ['manager', 'admin']