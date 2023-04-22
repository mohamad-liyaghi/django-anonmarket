from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from accounts.models import Account
from vote.models import Vote
from django_countries.fields import CountryField


class Product(models.Model):

    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    picture = models.ImageField(upload_to="products/%Y-%m-%d", blank=True, null=True)

    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name="products", blank=True, null=True)
    shipping_origin = CountryField()
    shipping_destinations = CountryField(blank=True, null=True)
    
    provider = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True, related_name="products")

    price = models.IntegerField(default=0)
    is_available = models.BooleanField(default=False)

    votes = GenericRelation(Vote, related_query_name="product_vote")

    def __str__(self):
        return self.title


class Category(models.Model):

    parent = models.ForeignKey('self', default=None, null=True, blank=True, on_delete=models.SET_NULL,
                               related_name='children')

    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120)

    def __str__(self):
        return self.title