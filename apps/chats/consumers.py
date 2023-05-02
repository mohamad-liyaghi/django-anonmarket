import json
from django.shortcuts import get_object_or_404
from channels.generic.websocket import WebsocketConsumer
from chats.models import Chat, Message


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        chat_id = self.scope["url_route"]["kwargs"]["id"]
        chat_code = self.scope["url_route"]["kwargs"]["code"]
        user = self.scope['user']

        self.room = get_object_or_404(user.chats.all(), id=chat_id, code=chat_code)
        
        self.chat_group_name = f'chat_{chat_id}_{chat_code}'

        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        # TODO add message to db
        pass