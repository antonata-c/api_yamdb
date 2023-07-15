from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Проверка доступа по роли admin."""

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.is_admin()
                     or request.user.is_superuser
                     or request.user.is_staff))


class ReadOnly(permissions.BasePermission):
    """Позволяет анониму совершать только безопасные запросы."""

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsAdminModeratorOwnerOrReadOnly(permissions.BasePermission):
    """Проверка доступа администратора, модератора, или владельца."""

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
                and (request.user.is_superuser
                     or request.user.is_staff
                     or request.user.is_admin()
                     or request.user.is_moderator()
                     or request.user == obj.author))
