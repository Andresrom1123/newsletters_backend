from rest_framework import serializers

from newslettersapp.models import Newsletter
from tags.serializers import TagSerializer
from users.serializers import UserSerializer


class NewsletterSerializer(serializers.ModelSerializer):
    tag = TagSerializer(read_only=True)
    users = UserSerializer(read_only=True, many=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = Newsletter
        fields = '__all__'


class CreateNewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = ['id', 'name', 'description', 'image', 'target', 'tag', 'author', 'frequency']
