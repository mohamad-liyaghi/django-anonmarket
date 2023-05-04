from django.test import TestCase
from accounts.models import Account
from chats.models import Chat, Message


class ChatTestCase(TestCase):
    def setUp(self) -> None:
        self.user_a = Account.objects.create(username='test username', password='1234EErr')
        self.user_b = Account.objects.create(username='test username2', password='1234EErr')
        self.chat = Chat.objects.create()
        self.chat.participants.set([self.user_a, self.user_b])
        self.message = Message.objects.create(sender=self.user_a, chat=self.chat, text="HI!")
        

    def test_chat_code_generator(self):
            self.assertTrue(self.chat.code)

    def test_message_code_generator(self):
            self.assertTrue(self.message.code)

    def test_edit_message(self):
          self.assertFalse(self.message.is_edited)
          self.message.text = 'New text.'
          self.message.save()
          self.assertTrue(self.message.is_edited)