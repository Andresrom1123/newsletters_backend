from rest_framework import serializers

from newslettersapp.models import Newsletter
from tags.serializers import TagSerializer
from users.serializers import UserAuthorSerializer


class NewsletterSerializer(serializers.ModelSerializer):
    tag = TagSerializer(read_only=True)
    vote = UserAuthorSerializer(read_only=True, many=True)
    subscribed = UserAuthorSerializer(read_only=True, many=True)
    author = UserAuthorSerializer(read_only=True)

    class Meta:
        model = Newsletter
        fields = '__all__'


class CreateNewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = ['id', 'name', 'created_at', 'description', 'image', 'target', 'tag', 'author']
