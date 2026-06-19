from rest_framework import permissions

class IsStaffOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow staff or admins to access the view.
    Maps to the 'Users Layer' in your architecture diagram.
    """
    def has_permission(self, request, view):
        # Check if user is authenticated first
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Check roles defined in our CustomUser model
        return request.user.role in ['staff', 'admin']