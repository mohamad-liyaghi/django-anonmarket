from django.db import models
from authentication.models import Account


class Chat(models.Model):
    '''chat model for users in order to send messages'''

    creator = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="chat_creator" ,blank=True, null=True)
    member = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="chat_member" ,blank=True, null=True)
    code = models.IntegerField()

    def __str__(self):
        return f"{self.creator} | {self.member}"