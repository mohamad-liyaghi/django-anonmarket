from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from votes.managers import VoteManager


class Vote(models.Model):
    '''Generic vote model'''

    class Choice(models.TextChoices):
        UPVOTE = ("u", "UpVote")
        DOWNVOTE = ("d", "DownVote")

    choice = models.CharField(max_length=1, choices=Choice.choices, default=Choice.UPVOTE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='votes')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    objects = VoteManager()

    def __str__(self) -> str:
        return self.choice
    
    class Meta:
        unique_together = ['user', 'content_type', 'object_id']