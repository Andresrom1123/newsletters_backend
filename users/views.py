from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from users.models import CustomUser
from users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Regresa una instancia de un usuario de acuerdo al ID mandado.
    list:
        Regresa la lista de usuario en la base de datos.
    create:
        Crea un usuario en la base de datos.
    delete:
        Elimina un usuario.
    update:
        Actualiza un libro.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        permissions = [IsAuthenticated]
        if self.request.user is not IsAuthenticated and self.request.method == 'POST':  # Si el usuario no esta autenticando y el método es un post
            permissions = [AllowAny]  # Los permisos estarán abiertos
        return [permission() for permission in permissions]

    @action(detail=False)  # users/is_active
    def is_active(self, request):
        """
            Regresa los usuarios inactivos
        """
        users = self.get_queryset().filter(is_active=False)
        serialized = UserSerializer(users, many=True)
        return Response(status=status.HTTP_200_OK, data=serialized.data)


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def activate_token(request, token):
    """
    Activa el correo de un usuario
    """
    user = get_object_or_404(CustomUser, token=token)
    user.is_active = True
    user.reset_token()
    user.save()
    return Response(status=status.HTTP_200_OK)
