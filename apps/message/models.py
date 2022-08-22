from django.db import models
from authentication.models import Account


class Chat(models.Model):
    '''chat model for users in order to send messages'''

    creator = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="chat_creator" ,blank=True, null=True)
    member = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="chat_member" ,blank=True, null=True)
    code = models.IntegerField()

    def __str__(self):
        return f"{self.creator} | {self.member}"


class Message(models.Model):
    '''Message text model'''

    text = models.TextField()
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="chats", blank=True,null=True)
    sender = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="messages", blank=True,null=True)

    is_edited = models.BooleanField(default=False)
    is_seen = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pk} | {self.sender.username}"


