from django.db import models
from django.utils import timezone

from tags.models import Tag
from users.models import CustomUser


class Newsletter(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    image = models.ImageField(verbose_name='Image Newsletter')
    meta = models.IntegerField()
    target = models.IntegerField()
    frequency = models.CharField(max_length=50)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_created=timezone.now)

    def __str__(self):
        return self.name


class NewslettersUser(models.Model):
    newsletter = models.ManyToManyField(Newsletter, related_name='newsletter_user')
    user = models.ManyToManyField(CustomUser, related_name='user_newsletter')
