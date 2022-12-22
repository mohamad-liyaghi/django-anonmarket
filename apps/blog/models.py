from django.db import models
from django.contrib.contenttypes.fields import GenericRelation

from vendor.models import Product
from authentication.models import Account
from vote.models import Vote


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

    vote = GenericRelation(Vote, related_query_name="account_vote")


    def __str__(self):
        return self.title


class Comment(models.Model):
    '''Base comment model'''

    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class ArticleComment(Comment):
    """Comment model for articles"""

    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="article_comment", blank=True, null=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comments", blank=True, null=True)

    def __str__(self):
        return f"{self.article} | {self.user}"