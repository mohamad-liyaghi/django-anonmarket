from django.contrib import admin
from customer.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("code", "customer", "status")