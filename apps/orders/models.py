from django.db import models
from products.models import Product
from accounts.models import Account
from orders.utils import unique_order_token_generator

class Order(models.Model):

    class STATUS(models.TextChoices):
        ORDERED = 'o', 'Ordered'
        ACCEPTED = 'a', 'Accepted'
        DECLINED = 'd', 'Declined'
        PREPARING = 'p', 'Preparing'
        SHIPPED = 's', 'Shipped'

    description = models.TextField(max_length=50, blank=True, null=True)
    token = models.CharField(max_length=20, unique=True, blank=True, null=True)

    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="orders", blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, related_name="orders", blank=True, null=True)
    provider = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)

    price = models.PositiveIntegerField()
    status = models.CharField(max_length=1, choices=STATUS.choices, default=STATUS.ORDERED)

    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.token)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.token = unique_order_token_generator(self.__class__)
            self.provider = self.product.provider
            self.price = self.product.price
            
        
        return super().save(*args, **kwargs)