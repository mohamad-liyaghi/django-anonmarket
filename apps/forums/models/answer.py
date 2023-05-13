from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from accounts.models import Account
from .forum import Forum
from forums.utils import unique_token_generator
from votes.models import Vote

class ForumAnswer(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='forum_answers')
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name='answers')
    answer = models.TextField()
    
    date = models.DateTimeField(auto_now=True)
    token = models.CharField(max_length=20, unique=True)

    is_edited = models.BooleanField(default=False)
    is_correct_answer = models.BooleanField(default=False)

    votes = GenericRelation(Vote, related_query_name="forum_answer_vote")

    def save(self, *args, **kwargs):
        if not self.pk:
            self.token = unique_token_generator(self.__class__)
            return super().save(*args, **kwargs)

        self.is_edited = True
        return super().save(*args, **kwargs)
    