from django.contrib import admin
from message.models import Chat, Message


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ("creator", "member", "code")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("chat", "sender", "is_seen")