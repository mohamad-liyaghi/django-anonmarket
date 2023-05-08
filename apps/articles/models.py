from django.db import models
from django.contrib.contenttypes.fields import GenericRelation

from products.models import Product
from accounts.models import Account
from votes.models import Vote
from comment.models import Comment
from articles.utils import unique_slug_generator

class Article(models.Model):
    '''The article model'''

    title = models.CharField(max_length=250)
    slug = models.SlugField()

    body = models.TextField()

    author = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="articles", blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="articles", blank=True, null=True)

    # this field is just for vip blogs
    price = models.IntegerField(default=0)
    allowed_members = models.ManyToManyField(Account, blank=True, related_name="allowed_members")

    published = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    votes = GenericRelation(Vote, related_query_name="account_vote")
    comment = GenericRelation(Comment)


    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = unique_slug_generator(self.title, self.__class__)
            
        return super().save(*args, **kwargs)
