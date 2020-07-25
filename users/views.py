from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny

from users.models import CustomUser
from users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        permissions = [IsAuthenticated]
        if self.request.user is not IsAuthenticated and self.request.method == 'POST':
            permissions = [AllowAny]
        return [permission() for permission in permissions]
