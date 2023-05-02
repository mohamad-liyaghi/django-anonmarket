import json
from channels.generic.websocket import AsyncWebsocketConsumer
from chats.models import Message
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        chat_id = self.scope["url_route"]["kwargs"]["id"]
        chat_code = self.scope["url_route"]["kwargs"]["code"]
        self.user = self.scope['user']

        self.chat = await self.get_chat(chat_id, chat_code)

        self.chat_group_name = f'chat_{chat_id}_{chat_code}'

        # TODO add group

        await self.accept()

    async def disconnect(self, close_code):
        # TODO remove group
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        if (text:=data['message']):
            await self.create_message(text)

    @database_sync_to_async
    def get_chat(self, chat_id, chat_code):
        return self.user.chats.filter(id=chat_id, code=chat_code).first()

    @database_sync_to_async
    def create_message(self, text):
        return Message.objects.create(chat=self.chat, sender=self.user, text=text)
