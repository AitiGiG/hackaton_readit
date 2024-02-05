from rest_framework import permissions


class IsVIPUser(permissions.BasePermission):
    """
    Разрешение, которое позволяет доступ только VIP пользователям.
    """

    def has_permission(self, request, view):

        return bool(
            request.method in permissions.SAFE_METHODS or
            request.user and request.user.is_authenticated and request.user.is_vip
        )

    def has_object_permission(self, request, view, obj):
 
        return bool(
            request.method in permissions.SAFE_METHODS or
            obj.user == request.user and request.user.is_vip
        )