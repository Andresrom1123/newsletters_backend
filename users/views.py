from django.db.models import F, Q
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from newslettersapp.models import Newsletter
from newslettersapp.serializers import NewsletterSerializer
from users.models import CustomUser
from users.tasks import send_email, send_email_reset_password
from users.permissions import UserPermissions
from users.serializers import UserSerializer, UserCreateSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Return a user with the id.
    list:
        Return the list of user in the bd.
    create:
        Create a user in the bd.
    delete:
        Delete a user.
    update:
        Update a user.
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
            Return the users that not are staff
        """
        users = CustomUser.objects.filter(is_staff=False)
        serialized = UserSerializer(users, many=True)
        return Response(status=status.HTTP_200_OK, data=serialized.data)

    @action(detail=True, methods=['GET'])
    def voted(self, request, pk=None):
        """
            Return the newsletters that voted a user
        """
        user = CustomUser.objects.get(id=pk)
        newsletter = Newsletter.objects.filter(
            Q(users=user) & Q(subscribed__lt=F('target'))
        )
        serialized = NewsletterSerializer(newsletter, many=True)
        return Response(status=status.HTTP_200_OK, data=serialized.data)

    @action(detail=True, methods=['GET'])
    def subscribed(self, request, pk=None):
        """
            Return the newsletter that subscribed a user
        """
        user = CustomUser.objects.get(id=pk)
        newsletter = Newsletter.objects.filter(
            Q(users=user) & Q(subscribed=F('target'))
        )
        serialized = NewsletterSerializer(newsletter, many=True)
        return Response(status=status.HTTP_200_OK, data=serialized.data)

    @action(detail=True, methods=['GET'])
    def author(self, request, pk=None):
        """
            Return the newsletter of a author.
        """
        user = CustomUser.objects.get(id=pk)
        author = user.author_newsletter.all()
        serialized = NewsletterSerializer(author, many=True)
        return Response(status=status.HTTP_200_OK, data=serialized.data)

    @action(detail=True, methods=['POST'])
    def staff(self, request, pk=None):
        """
            Change is_staff for True if the user is not staff.
        """
        user = CustomUser.objects.get(id=pk)
        if not user.is_staff:
            send_email.apply_async(args=[user.email])
            user.is_staff = True
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'The user is staff'})

    @action(detail=False, methods=['POST'])
    def email_reset_password(self, request):
        """
            Send the email and token to the task
        """
        email = request.data.get('email')
        user = CustomUser.objects.get(email=email)
        send_email_reset_password.apply_async(args=[email, user.token])
        return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def activate_token(request, token):
    """
        Activate the email of a user.
    """
    user = get_object_or_404(CustomUser, token=token)
    user.is_active = True
    user.reset_token()
    user.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def reset_password(request, token):
    """
        Change the password to a user
    """
    new_password = request.data.get('password')
    user = get_object_or_404(CustomUser, token=token)
    user.set_password(new_password)
    user.reset_token()
    user.save()
    return Response(status=status.HTTP_200_OK)
