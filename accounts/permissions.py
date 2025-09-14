from rest_framework import permissions

class IsOrganizerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.userprofile.role in ['organizer', 'admin']
        )

class IsAdmin(permissions.BasePermission):
    """
    Allow only users with user.userprofile.role == 'admin'
    """
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        try:
            return getattr(user.userprofile, 'role', None) == 'admin'
        except Exception:
            return False

class IsOrganizer(permissions.BasePermission):
    """
    Allow organizers and admins.
    """
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        try:
            return getattr(user.userprofile, 'role', None) in ('organizer', 'admin')
        except Exception:
            return False

class IsParticipant(permissions.BasePermission):
    """
    Allow only participants (students). Admins typically allowed where necessary.
    """
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        try:
            return getattr(user.userprofile, 'role', None) == 'student'
        except Exception:
            return False