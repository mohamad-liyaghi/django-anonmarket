from django.db import models

from authentication.models import Account
from blog.models import Comment, Rate


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


    def __str__(self):
        return self.title


class ForumComment(Comment):
    """Comment model for Forums"""

    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="forum_comment",
                             blank=True, null=True)

    forum = models.ForeignKey(Forum, on_delete=models.CASCADE,
                              related_name="comments", blank=True, null=True)

    def __str__(self):
        return f"{self.forum} | {self.user}"


class ForumRate(Rate):
    '''Like or dislike a forum'''

    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="forum_rate")
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name="likes")

    def __str__(self):
        return self.user.username