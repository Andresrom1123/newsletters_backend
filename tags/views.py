from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, F

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
    def newsletters_vote(self, request, slug=None):
        """
            Regresa los boletines que se pueden votar de un tag por el slug
        """
        tags = Tag.objects.get(slug=slug)  # Regresa un tag en particular por el slug
        newsletters = Newsletter.objects.filter(
            Q(tag__slug=tags.slug) & Q(subscribe__lt=F('target'))
        )  # filtramos los boletines por el tag__slug y los bolotines que el subscribe sea menor al target
        serialized = NewsletterSerializer(newsletters, many=True)
        return Response(status=status.HTTP_200_OK, data=serialized.data)

    @action(detail=True, methods=['GET'])
    def newsletters_subscribed(self, request, slug=None):
        """
            Regresa los boletines que se pueden votar de un tag por el slug
        """
        tags = Tag.objects.get(slug=slug)  # Regresa un tag en particular por el slug
        newsletters = Newsletter.objects.filter(
            Q(tag__slug=tags.slug) & Q(subscribe=F('target'))
        )  # filtramos los boletines por el tag__slug y los bolotines que el subscribe sea igual al target
        serialized = NewsletterSerializer(newsletters, many=True)
        return Response(status=status.HTTP_200_OK, data=serialized.data)
