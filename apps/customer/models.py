from django.db import models
from vendor.models import Product
from authentication.models import Account


class Order(models.Model):
    '''Order model that users can order things'''

    class Status(models.TextChoices):
        ordered  = ("o", "Ordered ")
        accepted = ("a", "Accepted")
        rejected = ("r", "Rejected")
        paid = ("p", "Paid")
        sent = ("s", "Sent")

    code = models.CharField(max_length=20, unique=True, blank=True, null=True)
    item = models.ForeignKey(Product, on_delete=models.SET_NULL, related_name="orders", blank=True, null=True)

    price = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    status = models.CharField(max_length=1, choices=Status.choices, default=Status.ordered)
    customer = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="orders",blank=True, null=True)

    description = models.TextField()

    def __str__(self):
        return str(self.code)

