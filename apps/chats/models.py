from django.db import models
from accounts.models import Account


class Chat(models.Model):
    '''chat model for users in order to send messages'''

    code = models.IntegerField()
    participants = models.ManyToManyField(Account, related_name='rooms')

    def __str__(self):
        return str(self.code)


class Message(models.Model):
    '''Message text model'''

    text = models.TextField()
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages", blank=True, null=True)
    sender = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="messages", blank=True, null=True)

    is_edited = models.BooleanField(default=False)
    is_seen = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pk} | {self.sender.username}"
    
    def save(self, *args, **kwargs):
        if self.pk:
            self.is_edited = True

        return super().save(*args, **kwargs)