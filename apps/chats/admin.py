from django.contrib import admin
from chats.models import Chat, Message, Notification, ChatParticipant


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ("code",)

@admin.register(ChatParticipant)
class ChatParticipantAdmin(admin.ModelAdmin):
    list_display = ("user", 'chat')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("chat", "sender", "is_seen")

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("chat", "account", "is_active")