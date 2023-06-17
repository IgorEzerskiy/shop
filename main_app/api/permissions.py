from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            (request.user.is_staff or request.user.is_superuser)
        )


class IsAdminOrPermissionDenied(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            (request.user.is_staff or request.user.is_superuser)
        )


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or (request.user.is_staff or request.user.is_superuser)
