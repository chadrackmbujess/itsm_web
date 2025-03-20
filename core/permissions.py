from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permission personnalisée qui permet aux admins de modifier,
    mais aux utilisateurs normaux seulement de voir les données.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True  # Lecture autorisée pour tout le monde
        return request.user and request.user.is_staff  # Modification réservée aux admins
