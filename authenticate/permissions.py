from rest_framework import permissions
from .models import User, PacjentProfil, LekarzProfil

class LekarzPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if obj.type == User.Types.LEKARZ or obj.type == User.Types.ADMIN:
            return True
        return False

    #def has_permission(self, request, view):