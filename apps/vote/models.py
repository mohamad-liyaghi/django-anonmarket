from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from vote.managers import VoteManager

class Vote(models.Model):
    '''A vote model that can be used for products, users, etc.'''

    class Choice(models.TextChoices):
        like = ("l", "Like")
        dislike = ("d", "Dislike")

    vote = models.CharField(max_length=1, choices=Choice.choices, default=Choice.like)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    objects = VoteManager()

    def __str__(self) -> str:
        return self.vote