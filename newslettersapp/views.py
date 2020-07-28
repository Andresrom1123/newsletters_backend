from rest_framework import viewsets

from newslettersapp.models import Newsletter
from newslettersapp.serializers import NewsletterSerializer


class NewsletterViewSet(viewsets.ModelViewSet):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer
