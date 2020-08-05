from rest_framework import viewsets

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
