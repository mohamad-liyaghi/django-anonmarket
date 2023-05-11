from django.contrib import admin
from forums.models import Forum


@admin.register(Forum)
class ForumAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ("title", "author", "closed")
