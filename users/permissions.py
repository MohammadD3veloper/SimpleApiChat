from rest_framework.permissions import (
    SAFE_METHODS, BasePermission
)

class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsStaffOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return super(IsStaffOrReadOnly, self).has_permission(request, view)
        return request.method in SAFE_METHODS
