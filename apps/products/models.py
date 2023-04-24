from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.text import slugify
from django_countries.fields import CountryField

from accounts.models import Account
from vote.models import Vote
from products.utils import unique_slug_generator


class Product(models.Model):

    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    picture = models.ImageField(upload_to="products/%Y-%m-%d", blank=True, null=True)

    category = models.ForeignKey("Category", on_delete=models.SET_NULL, related_name="products", blank=True, null=True)
    shipping_origin = CountryField()
    shipping_destinations = CountryField(blank=True, null=True)
    
    provider = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True, related_name="products")

    price = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=False)

    vote = GenericRelation(Vote, related_query_name="product_vote")

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        
        # When user changes the title, slug will be updated too.
        if not self.slug or slugify(self.title) not in self.slug:
            self.slug = unique_slug_generator(title=self.title, cls=self.__class__)

        return super().save(*args, **kwargs)


class Category(models.Model):

    parent = models.ForeignKey(
        'self', default=None, null=True, blank=True, on_delete=models.SET_NULL, related_name='children'
    )
    
    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.title = self.title.lower()
        self.slug = unique_slug_generator(self.title, self.__class__)
        return super().save(*args, **kwargs)