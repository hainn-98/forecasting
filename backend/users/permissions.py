from rest_framework.permissions import BasePermission


class UserPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        current_user = request.user
        if current_user.role == 2:
            return current_user.client == obj.client
        elif current_user == obj:
            return True
        return False

class OwnerPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        current_user = request.user
        return current_user==obj

class AdminPermission(BasePermission):
    def has_permission(self, request, view):
        current_user = request.user
        return current_user.role >1
    