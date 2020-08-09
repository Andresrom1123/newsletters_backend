from django.db import models
from django.utils import timezone

from tags.models import Tag
from users.models import CustomUser


class Newsletter(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    image = models.ImageField(verbose_name='Image Newsletter')
    subscribe = models.IntegerField(default=0)
    target = models.IntegerField()
    frequency = models.CharField(
        max_length=2,
        choices=[
            ('Dy', 'DAILY'),
            ('Wy', 'WEEKLY'),
            ('My', 'MONTHLY')
        ]
    )
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    vote = models.ManyToManyField(CustomUser, related_name='user_newsletter_vote', blank=True)
    subscribed = models.ManyToManyField(CustomUser, related_name='user_newsletter_subscribed', blank=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='author_newsletter')
    created_at = models.DateTimeField(auto_created=timezone.now)

    def __str__(self):
        return self.name
