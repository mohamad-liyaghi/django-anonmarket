from django.contrib import admin
from blog.models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "published")
    prepopulated_fields = {"slug" : ("title",)}