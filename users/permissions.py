from rest_framework.permissions import BasePermission


class UserPermissions(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated and request.method == 'POST':
            return True
        if request.user.is_admin and view.action in ['list', 'staff']:
            return True
        if request.user.is_staff and view.action in ['author']:
            return True

    def has_object_permission(self, request, view, obj):
        pass
