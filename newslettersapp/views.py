from rest_framework import viewsets

from newslettersapp.models import Newsletter
from newslettersapp.serializers import NewsletterSerializer


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
