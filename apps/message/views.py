from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404, render
from django.db.models import Q

import random

from authentication.models import Account
from message.models import Chat
from .forms import MessageForm


class ChatList(LoginRequiredMixin, TemplateView):
    '''Show All Available chats of a user'''
    template_name = "message/chat-list.html"


    def get_context_data(self, **kwargs):
        context = super(ChatList, self).get_context_data(**kwargs)

        context['creator_chats'] = self.request.user.chat_member.all()
        context['member_chats'] = self.request.user.chat_creator.all()


        return context



class GetChat(LoginRequiredMixin, View):
    '''Create or Connect a user to a chat'''

    def get(self, request, id, token):
        # get the user that we want to connect
        user = get_object_or_404(Account, id=id, token=token)

        # check if this chat has created before
        existing_chat = Chat.objects.filter(Q(creator= user) & Q(member= self.request.user)
                                             | Q(creator= self.request.user) & Q(member= user))

        # if this chat is new, we create a new chat
        if not existing_chat.exists():
            existing_chat = Chat.objects.create(creator= self.request.user, member= user,
                                code= random.randint(-2147483648, 2147483647))
        else:
            existing_chat = existing_chat.first()

        # then we redirect to the chat detail page
        return redirect("message:chat-detail", existing_chat.pk, existing_chat.code)



class ChatDetail(LoginRequiredMixin, View):
    '''Page of a chat that user can send, read a message'''

    def setup(self, request, *args, **kwargs):
        '''Get The chat'''
        self.chat = get_object_or_404(Chat, Q(id= kwargs["id"]) & Q(code=kwargs["code"])
                                 & Q(creator=request.user) | Q(member=request.user))

        return super().setup(request, *args, **kwargs)


    def get(self, request, id, code):
        """Return the messages of a chat"""

        messages = self.chat.chats.all().order_by("-date") [:50]

        form = MessageForm

        return render(self.request, "message/chat-detail.html", {"all_messages" : messages, "chat" : self.chat, "form" : form})



    def post(self, request, *args, **kwargs):
        '''Create a message in chat'''

        form = MessageForm(self.request.POST)

        if form.is_valid():
            form = form.save(commit=False)
            form.chat = self.chat
            form.sender = self.request.user
            form.save()

        return redirect("message:chat-detail", self.chat.pk, self.chat.code)
