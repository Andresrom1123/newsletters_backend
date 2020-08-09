from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from newslettersapp.models import Newsletter
from newslettersapp.serializers import NewsletterSerializer
from tags.models import Tag
from tags.serializers import TagSerializer


class TagViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Regresa una instancia de una etiqueta de acuerdo al ID mandado.
    list:
        Regresa la lista de etiquetas en la base de datos.
    create:
        Crea una etiqueta en la base de datos.
    delete:
        Elimina una etiqueta.
    update:
        Actualiza una etiqueta.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = 'slug'

    @action(detail=True, methods=['GET'])
    def newsletters(self, request, slug=None):
        """
            Regresa los boletines de un tag por el slug
        """
        tags = Tag.objects.get(slug=slug)  # Regresa un tag en particular por el slug
        newsletters = Newsletter.objects.filter(tag__slug=tags.slug)  # filtramos los boletines por el tag__slug
        serialized = NewsletterSerializer(newsletters, many=True)
        return Response(status=status.HTTP_200_OK, data=serialized.data)
