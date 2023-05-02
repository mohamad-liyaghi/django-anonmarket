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

        await self.channel_layer.group_add(
            self.chat_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        if (text:=data['message']):
            await self.add_message_to_db(text)

    @database_sync_to_async
    def get_chat(self, chat_id, chat_code):
        return self.user.chats.filter(id=chat_id, code=chat_code).first()

    @database_sync_to_async
    def create_message(self, text):
        return Message.objects.create(chat=self.chat, sender=self.user, text=text)

    async def add_message_to_db(self, text):
        message = await self.create_message(text)
        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'chat_message',
                'text': message.text,
                'sender': message.sender.username,
                'date': str(message.date),
                'is_seen': str(message.is_seen),
                'is_edited': str(message.is_edited),
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))
