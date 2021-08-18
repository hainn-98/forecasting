from rest_framework.permissions import BasePermission


class OwnerPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        current_user = request.user
        return current_user==obj.creator

class ExpertPermission(BasePermission):
    def has_permission(self, request, view):
        current_user = request.user
        return current_user.role == 1