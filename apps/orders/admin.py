from django.contrib import admin
from orders.models import Order


@admin.register(Order)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ("token", "account", "status")