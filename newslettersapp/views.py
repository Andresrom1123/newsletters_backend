from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import F

from core.pagination import StandardResultsSetPagination
from newslettersapp.models import Newsletter
from newslettersapp.permissions import NewsletterPermissions
from newslettersapp.serializers import NewsletterSerializer, CreateNewsletterSerializer
from users.models import CustomUser


class NewsletterViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Return a newsletter of a user with the id.
    list:
        Return the list of newsletter in the bd.
    create:
        Create a newsletter in the bd.
    delete:
        Delete a newsletter.
    update:
        Update a newsletter.
    """
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer
    permission_classes = [NewsletterPermissions]
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        # retrieve
        if self.action == 'create':
            return CreateNewsletterSerializer
        else:
            return NewsletterSerializer

    @action(detail=True, methods=['POST'])
    def subscribed(self, request, pk=None):
        """
            Add at user the newsletter subscribed
        """
        newsletter = Newsletter.objects.get(id=pk)
        user_id = request.data.get('user')
        user = CustomUser.objects.get(id=user_id)
        if not newsletter.subscribed.filter(id=user.id).exists() and newsletter.subscribe == newsletter.target:
            newsletter.subscribed.add(user)
        elif newsletter.subscribed.filter(id=user.id).exists():
            newsletter.subscribed.remove(user)
        newsletter.save()
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'])
    def vote(self, request, pk=None):
        """
            Add the user that voted for a newsletter
        """
        newsletter = Newsletter.objects.get(id=pk)
        user_id = request.data.get('user')
        user = CustomUser.objects.get(id=user_id)
        if not newsletter.vote.filter(id=user.id).exists() and newsletter.subscribe < newsletter.target:
            newsletter.subscribe += 1
            newsletter.vote.add(user)
        elif newsletter.vote.filter(id=user.id).exists():
            newsletter.vote.remove(user)
            if not newsletter.subscribe == newsletter.target:
                newsletter.subscribe -= 1
        newsletter.save()
        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def vote_get(self, request):
        """
            Return a list the newsletters that can vote
        """
        newsletters = self.get_queryset().filter(subscribe__lt=F('target'))
        serialized = NewsletterSerializer(newsletters, many=True)
        return Response(status=status.HTTP_200_OK, data=serialized.data)

    @action(detail=False, methods=['GET'])
    def subscribed_get(self, request):
        """
            Return the newsletters that can subscribe
        """
        newsletters = Newsletter.objects.filter(subscribe=F('target'))
        serialized = NewsletterSerializer(newsletters, many=True)
        return Response(status=status.HTTP_200_OK, data=serialized.data)
