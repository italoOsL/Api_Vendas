from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser
    
class IsUserPro(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_staff
    
class IsUserDefault(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS
    
class IsAdminOrUserPro(BasePermission):
    def has_permission(self, request, view):
        return request.user and (request.user.is_superuser or request.user.is_staff)
