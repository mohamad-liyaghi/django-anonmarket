from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.db.models import Q

import random

from authentication.models import Account
from message.models import Chat


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

        # then we redirect to the chat detail page
        return redirect("message:chat-detail", existing_chat.pk, existing_chat.code)



