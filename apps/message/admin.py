from django.contrib import admin
from message.models import Chat


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ("creator", "member", "code")