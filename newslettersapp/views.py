from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import F

from core.pagination import StandardResultsSetPagination
from newslettersapp.models import Newsletter
from newslettersapp.permissions import NewsletterPermissions
from newslettersapp.serializers import NewsletterSerializer, CreateNewsletterSerializer
from users.models import CustomUser
from newslettersapp.tasks import send_email_newsletter
from users.serializers import UserSerializer


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
        if self.action == 'create':
            return CreateNewsletterSerializer
        else:
            return NewsletterSerializer

    @action(detail=True, methods=['POST'])
    def subscribe(self, request, pk=None):
        """
            Add at user the newsletter subscribe
        """
        newsletter = Newsletter.objects.get(id=pk)
        user_id = request.data.get('user')
        user = CustomUser.objects.get(id=user_id)
        if not newsletter.users.filter(id=user.id).exists() and newsletter.subscribed == newsletter.target:
            newsletter.users.add(user)
        elif newsletter.users.filter(id=user.id).exists():
            newsletter.users.remove(user)
        newsletter.save()
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'])
    def vote(self, request, pk=None):
        """
            Add the user that vote for a newsletter
        """
        newsletter = Newsletter.objects.get(id=pk)
        user_id = request.data.get('user')
        user = CustomUser.objects.get(id=user_id)
        if not newsletter.users.filter(id=user.id).exists() and newsletter.subscribed < newsletter.target:
            newsletter.users.add(user)
            if (newsletter.target-newsletter.subscribed) == 1:
                serialized_user = UserSerializer(newsletter.users.all(), many=True)
                serialized_newsletter = NewsletterSerializer(newsletter)
                send_email_newsletter.apply_async(args=[serialized_user.data, serialized_newsletter.data])
            newsletter.subscribed += 1
        elif newsletter.users.filter(id=user.id).exists():
            newsletter.users.remove(user)
            if not newsletter.subscribed == newsletter.target:
                newsletter.subscribed -= 1
        newsletter.save()
        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def vote_get(self, request):
        """
            Return a list the newsletters that can vote
        """
        newsletters = self.get_queryset().filter(subscribed__lt=F('target'))
        serialized = NewsletterSerializer(newsletters, many=True)
        return Response(status=status.HTTP_200_OK, data=serialized.data)

    @action(detail=False, methods=['GET'])
    def subscribe_get(self, request):
        """
            Return the newsletters that can subscribe
        """
        newsletters = Newsletter.objects.filter(subscribed=F('target'))
        serialized = NewsletterSerializer(newsletters, many=True)
        return Response(status=status.HTTP_200_OK, data=serialized.data)
