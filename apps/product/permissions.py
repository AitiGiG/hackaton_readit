from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Проверяем, является ли пользователь сотрудником (is_staff) и является ли он владельцем объекта
        return obj.owner == request.user