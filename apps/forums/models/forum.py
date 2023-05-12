from django.db import models
from django.contrib.contenttypes.fields import GenericRelation

from accounts.models import Account
from votes.models import Vote
from forums.utils import unique_slug_generator


class Forum(models.Model):
    '''The Forum model'''

    title = models.CharField(max_length=250)
    slug = models.SlugField()

    body = models.TextField()

    author = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="forums", blank=True, null=True)

    closed = models.BooleanField(default=False)
    updated = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    votes = GenericRelation(Vote, related_query_name="forum_vote")

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = unique_slug_generator(self.title, self.__class__)
            return super().save(*args, **kwargs)
        
        self.updated = True
        return super().save(*args, **kwargs)
    