from django.db import models
from django.contrib.contenttypes.fields import GenericRelation

from products.models import Product
from accounts.models import Account
from votes.models import Vote
from comments.models import Comment
from articles.utils import unique_slug_generator, unique_token_generator


class Article(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=100)

    body = models.TextField()

    author = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="articles", blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="articles", blank=True, null=True)

    price = models.IntegerField(default=0)

    published = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now=True)

    votes = GenericRelation(Vote, related_query_name="article_votes")
    comments = GenericRelation(Comment)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = unique_slug_generator(self.title, self.__class__)
            
        return super().save(*args, **kwargs)


class ArticlePurchase(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='article_purchases')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='purchases')
    date = models.DateTimeField(auto_now=True)
    token = models.CharField(max_length=20, unique=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.token = unique_token_generator(self.__class__)
            # Exchange money
            self.user.balance -= self.article.price
            self.article.author.balance += self.article.price

            self.article.author.save()
            self.user.save()

        return super().save(*args, **kwargs)