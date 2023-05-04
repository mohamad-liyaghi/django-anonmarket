from django.dispatch import receiver
from django.db.models import Q
from django.db.models.signals import post_save

from chats.models import Message, Notification

@receiver(post_save, sender=Message)
def create_notification_for_message(sender, **kwargs):
    if kwargs["created"]:

        message = kwargs["instance"]
        chat = message.chat
        notification = chat.notifications.all()
        chat_participant = chat.participants.filter(~Q(id=message.sender.id)).first()

        if notification:
            user_notification = notification.filter(account=chat_participant).first()
            user_notification.is_active = True
            user_notification.save()

        else:

            chat.notifications.create(chat=chat, account=chat_participant, is_active=True)