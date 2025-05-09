from rest_framework import permissions


class Anonymous(permissions.BasePermission):
    """Разрешения для анонимных пользователей."""
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class Author(permissions.BasePermission):
    """Разрешения для пользователей с ролью автор."""

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return getattr(obj, "author", None) == request.user


class Administrator(permissions.BasePermission):
    """Разрешения для пользователей с ролью суперюзер"""
    def is_admin(self, request):
        return request.user.is_authenticated and request.user.is_staff

    def has_permission(self, request, view):
        return self.is_admin(request)

    def has_object_permission(self, request, view, obj):
        return self.is_admin(request)
