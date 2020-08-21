from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from newslettersapp.serializers import NewsletterSerializer
from users.models import CustomUser
from users.tasks import send_email
from users.permissions import UserPermissions
from users.serializers import UserSerializer, UserCreateSerializer


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
    permission_classes = [UserPermissions, ]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        else:
            return UserSerializer

    @action(detail=False, methods=['GET'])
    def no_staff(self, request):
        """
            Regresa los usuarios que no son staff
        """
        users = CustomUser.objects.filter(is_staff=False)
        serialized = UserSerializer(users, many=True)
        return Response(status=status.HTTP_200_OK, data=serialized.data)

    @action(detail=True, methods=['GET'])
    def vote(self, request, pk=None):
        """
        Regresa los boletines que ha votado un usuario
        """
        user = CustomUser.objects.get(id=pk)
        newsletter = user.user_newsletter_vote.all()
        serialized = NewsletterSerializer(newsletter, many=True)
        return Response(status=status.HTTP_200_OK, data=serialized.data)

    @action(detail=True, methods=['GET'])
    def subscribed(self, request, pk=None):
        """
        Regresa los boletines que se ha subscribido un usuario
        """
        user = CustomUser.objects.get(id=pk)
        newsletter = user.user_newsletter_subscribed.all()
        serialized = NewsletterSerializer(newsletter, many=True)
        return Response(status=status.HTTP_200_OK, data=serialized.data)

    @action(detail=True, methods=['GET'])
    def author(self, request, pk=None):
        """
        Regresa los boletines de un author
        """
        user = CustomUser.objects.get(id=pk)
        author = user.author_newsletter.all()
        serialized = NewsletterSerializer(author, many=True)
        return Response(status=status.HTTP_200_OK, data=serialized.data)

    @action(detail=False, methods=['POST'])
    def staff(self, request):
        """
        Cambia el is_staff a True si el usuario no es staff
        """
        user_id = request.data.get('user')
        user = CustomUser.objects.get(id=user_id)
        if not user.is_staff:
            send_email.apply_async()
            user.is_staff = True
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'The user is staff'})


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
