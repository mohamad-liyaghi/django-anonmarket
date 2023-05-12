from django.contrib import admin
from forums.models import Forum, ForumAnswer, ForumPurchase


@admin.register(Forum)
class ForumAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "closed")

@admin.register(ForumAnswer)
class ForumAnswerAdmin(admin.ModelAdmin):
    list_display = ("user", "forum", "token")

@admin.register(ForumPurchase)
class ForumPurchaseAdmin(admin.ModelAdmin):
    list_display = ("user", "forum", "token")