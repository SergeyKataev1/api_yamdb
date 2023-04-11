"""Проект спринта 10: модуль проверки разрешений приложения Api."""
from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Разрешение: просмотра и действий только для Администратора"""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsAdminOrReadOnly(permissions.BasePermission):
    """Разрешение: просмотра любой пользователь,
    действие только Администратор"""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_admin


class IsAuthorIsAdminIsModeratorOrReadOnly(permissions.BasePermission):
    """
    Разрешение действия для
    Автора, Mодератора, Администратора.
    Просмотр любой пользователь
    """
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            request.user.is_moderator
            or request.user.is_admin
            or obj.author == request.user
        )
