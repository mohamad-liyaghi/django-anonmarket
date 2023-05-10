from django.contrib import admin
from articles.models import Article, ArticlePurchase

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "published")
    
@admin.register(ArticlePurchase)
class ArticlePurchaseAdmin(admin.ModelAdmin):
    list_display = ("article", "user", "date")
    
