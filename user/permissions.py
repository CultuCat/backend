from rest_framework import permissions
from django.core.exceptions import ObjectDoesNotExist

class IsAuthenticated(permissions.IsAuthenticated):
    def has_permission(self, request, view=None):
        return super().has_permission(request, view) and request.user.is_active
    
        
class IsAdmin(IsAuthenticated):
    def has_permission(self, request, view=None):
        try:
            return super().has_permission(request, view) and request.user.is_staff
        except (ObjectDoesNotExist, AttributeError):
            return False
