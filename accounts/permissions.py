from rest_framework import permissions


from .models import User


class IsPatient(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.user.application_role == User.PATIENT:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        return True


class IsDoctor(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.user.application_role == User.DOCTOR:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        return True


class IsAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.user.is_authenticated)
