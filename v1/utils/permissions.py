from rest_framework.permissions import BasePermission


class IsManager(BasePermission):
    message = "You are not manager"

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.role == 'manager')


class IsAdmin(BasePermission):
    message = "You are not admin"

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.role == 'admin')
