from django.db import models

from authentication.models import Account


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