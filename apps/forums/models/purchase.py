from django.db import models
from accounts.models import Account
from .forum import Forum
from forums.utils import unique_token_generator


class ForumPurchase(models.Model):

    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='forum_purchases')
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name='purchases')
    date = models.DateTimeField(auto_now=True)
    token = models.CharField(max_length=20, unique=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            # Create token for object
            self.token = unique_token_generator(self.__class__)
            # Exchange money
            self.user.balance -= self.forum.price
            self.forum.author.balance += self.forum.price

            self.forum.author.save()
            self.user.save()

        return super().save(*args, **kwargs)