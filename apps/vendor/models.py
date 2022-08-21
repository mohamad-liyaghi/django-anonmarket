from django.db import models
from authentication.models import Account, Rate


class Category(models.Model):

    parent = models.ForeignKey('self', default=None, null=True, blank=True, on_delete=models.SET_NULL,
                               related_name='children')

    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, max_length=120)

    def __str__(self):
        return self.title


class Country(models.Model):
    '''supported countries that vendors ship product to'''

    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, max_length=120)

    def __str__(self):
        return self.name


class Product(models.Model):

    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120, blank=True, null=True)
    description = models.TextField()

    picture = models.ImageField(upload_to="products/%Y-%m-%d", blank=True, null=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products", blank=True, null=True)
    shipping_from = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="shipping_from", blank=True, null=True)
    shipping_to = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, null=True, related_name="shipping_to")
    seller = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True, related_name="products")

    price = models.IntegerField(default=0)
    is_available = models.BooleanField(default=False)

    def __str__(self):
        return self.title



class ProductRate(Rate):
    '''Like or dislike a product'''

    customer = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="product_rate")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="likes")

    def __str__(self):
        return self.customer.username