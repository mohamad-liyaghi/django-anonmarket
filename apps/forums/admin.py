from django.contrib import admin
from forums.models import Forum, ForumAnswer


@admin.register(Forum)
class ForumAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "closed")

@admin.register(ForumAnswer)
class ForumAnswerAdmin(admin.ModelAdmin):
    list_display = ("user", "forum", "token")
