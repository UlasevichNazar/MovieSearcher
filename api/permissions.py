from rest_framework import permissions


class IsOwnerUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff
