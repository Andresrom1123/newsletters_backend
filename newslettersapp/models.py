from django.db import models
from django.utils import timezone

from tags.models import Tag
from users.models import CustomUser


class Newsletter(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    image = models.ImageField(verbose_name='Image Newsletter')
    subscribe = models.IntegerField()
    target = models.IntegerField()
    frequency = models.CharField(max_length=50)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    vote = models.BooleanField(default=False)
    subscribed = models.BooleanField(default=False)
    user = models.ManyToManyField(CustomUser, related_name='user_newsletter', null=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='author_newsletter')
    created_at = models.DateTimeField(auto_created=timezone.now)

    def __str__(self):
        return self.name
