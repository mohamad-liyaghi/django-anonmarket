from django.contrib import admin
from products.models import Category, Product


admin.site.register(Category)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ("title", "provider", "price")
