from django.db import models
from django.utils import timezone

from tags.models import Tag
from users.models import CustomUser


class Newsletter(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=100)
    image = models.ImageField(verbose_name='Image Newsletter')
    subscribed = models.IntegerField(default=0)
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
    users = models.ManyToManyField(CustomUser, related_name='user_newsletter', blank=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='author_newsletter')
    created_at = models.DateTimeField(auto_created=timezone.now, auto_now_add=True)

    def __str__(self):
        return self.name
