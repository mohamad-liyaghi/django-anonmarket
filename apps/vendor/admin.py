from django.contrib import admin
from vendor.models import Category, Country, Product, ProductRate


admin.site.register(Category)
admin.site.register(Country)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ("title", "seller", "price")


@admin.register(ProductRate)
class ProductRateAdmin(admin.ModelAdmin):
    list_display = ("customer", "product", "vote")