from django.db import models
from django.contrib.contenttypes.fields import GenericRelation

from accounts.models import Account
from comment.models import Comment
from vote.models import Vote


class Forum(models.Model):
    '''The Forum model'''

    title = models.CharField(max_length=250)
    slug = models.SlugField()

    body = models.TextField()

    author = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="forums", blank=True, null=True)

    # this field is just for vip forums
    price = models.IntegerField(default=0)
    allowed_members = models.ManyToManyField(Account, blank=True, related_name="forum_allowed_members")

    closed = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    vote = GenericRelation(Vote, related_query_name="forum_vote")
    comment = GenericRelation(Comment)

    def __str__(self):
        return self.title


