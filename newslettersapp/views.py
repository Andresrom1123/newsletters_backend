from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from newslettersapp.models import Newsletter
from newslettersapp.serializers import NewsletterSerializer, CreateNewsletterSerializer
from users.models import CustomUser


class NewsletterViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Regresa un boletin de un usuario de acuerdo al ID mandado.
    list:
        Regresa la lista de boletines en la base de datos.
    create:
        Crea un boletin en la base de datos.
    delete:
        Elimina un boletin.
    update:
        Actualiza un boletin.
    """
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer

    def get_serializer_class(self):
        # retrieve
        if self.action == 'create':
            return CreateNewsletterSerializer
        else:
            return NewsletterSerializer

    @action(detail=True, methods=['POST'])
    def action(self, request, pk=None):
        """
            Agrega un boletin a un usuario
        """
        newsletter = Newsletter.objects.get(id=pk)
        user_id = request.data.get('user')
        user_1 = CustomUser.objects.get(id=user_id)
        if newsletter.user.filter(id=user_1.id).exists():
            newsletter.user.remove(user_1)
            if newsletter.vote:
                newsletter.vote = False
                newsletter.target -= 1
            elif newsletter.subscribed:
                newsletter.subscribed = False
        else:
            newsletter.user.add(user_1)
            if newsletter.target <= newsletter.meta and not newsletter.vote:
                newsletter.target += 1
                newsletter.vote = True
            elif newsletter.target > newsletter.meta and not newsletter.subscribed:
                newsletter.subscribed = True

        newsletter.save()
        return Response(status=status.HTTP_200_OK)
