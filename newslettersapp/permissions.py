from rest_framework.permissions import BasePermission, IsAuthenticated


class NewsletterPermissions(BasePermission):

    def has_permission(self, request, view):
        if request.user is not IsAuthenticated and view.action in ['list', 'vote_get', 'subscribed_get']:
            return True

        if request.user.is_staff and request.method in ['POST', 'DELETE', 'PATCH']:
            return True

    def has_object_permission(self, request, view, obj):
        pass
