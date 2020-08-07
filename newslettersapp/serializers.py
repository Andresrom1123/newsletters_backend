from rest_framework import serializers

from newslettersapp.models import Newsletter
from tags.serializers import TagSerializer
from users.serializers import UserSerializer


class NewsletterSerializer(serializers.ModelSerializer):
    tag = TagSerializer(read_only=True)
    user = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Newsletter
        fields = '__all__'


class CreateNewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = '__all__'
