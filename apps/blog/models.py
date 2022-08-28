from django.db import models

from vendor.models import Product
from authentication.models import Account, Rate


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


    def __str__(self):
        return self.title


class ArticleRate(Rate):
    '''Like or dislike an article'''

    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="article_rate")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="likes")

    def __str__(self):
        return self.customer.username