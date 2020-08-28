from rest_framework.permissions import BasePermission


class NewsletterPermissions(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated and view.action in ['list', 'vote_get', 'subscribe_get']:
            return True

        if request.user.is_staff and view.action in ['create', 'destroy', 'update', 'retrieve']:
            return True

        if request.user.is_authenticated and view.action in ['subscribe', 'vote']:
            return True

    def has_object_permission(self, request, view, obj):
        if obj.author == request.user:
            return True
