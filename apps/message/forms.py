from django.forms import ModelForm
from message.models import Message


class MessageForm(ModelForm):
    '''Create message form'''

    class Meta:
        model = Message
        fields = ["text", "chat", "sender"]

