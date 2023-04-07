"""Проект спринта 10: модуль проверки разрешений приложения Api."""
from rest_framework import permissions


class AuthorPermission(permissions.BasePermission):
    """Глобальная проверка разрешений для автора."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if obj.author == request.user:
            return True
        return False


class CategoryAndGenrePermission(permissions.BasePermission):
    """Глобальная проверка разрешений для моделей Category и Genre."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user.is_authenticated and request.user.is_admin)


class AdminPermission(permissions.BasePermission):
    """Глобальная проверка разрешений для Администратора."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and (
            request.user.is_admin or request.user.is_superuser)


class StrongPermission(permissions.BasePermission):
    """Глобальная проверка разрешений для модели Review."""

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        elif request.method == 'POST':
            return request.user.is_authenticated
        elif request.method in ['PATCH', 'DELETE']:
            return (
                request.user.is_moderator
                or request.user.is_admin
                or obj.author == request.user)
        return False


class IsAdmin(permissions.BasePermission):
    """Разрешение для UserViewSet"""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin or request.user.is_superuser)
