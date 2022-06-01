from rest_framework import permissions
from authenticate.models import User, PacjentProfil, LekarzProfil

class PacjenciPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        if obj.user == request.user:
            return True
        return False

    #def has_permission(self, request, view):


class BadaniePermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        if obj.pacjent.user == request.user:
            return True
        if request.user.type == User.Types.DIAGNOSTA:
            return True
        if request.user.type == User.Types.LEKARZ:
            profil = LekarzProfil.objects.get(pk=request.user)
            if profil.pacjenci.filter(pk = obj.pacjent.user):
                return True
        return False

    #def has_permission(self, request, view):

class BadaniaPacjentaPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        if obj.user == request.user:
            return True
        if request.user.type == User.Types.LEKARZ:
            profil = LekarzProfil.objects.get(pk=request.user)
            if profil.pacjenci.filter(pk = obj.user):
                return True
        return False

    #def has_permission(self, request, view):

class LaborantPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or request.user.type == User.Types.DIAGNOSTA:
            return True
        return False

    def has_permission(self, request, view):
        if request.user.is_staff or request.user.type == User.Types.DIAGNOSTA:
            return True
        return False

class DetailBadaniePermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        if obj.badanie.pacjent.user == request.user and request.method == 'GET':
            return True
        if request.user.type == User.Types.DIAGNOSTA:
            return True
        if request.user.type == User.Types.LEKARZ:
            profil = LekarzProfil.objects.get(pk=request.user)
            if profil.pacjenci.filter(pk = obj.badanie.pacjent.user) and request.method == 'GET':
                return True
        return False

    #def has_permission(self, request, view):