from typing import Any, Dict
from django.views.generic import ListView, View, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q 

from chats.models import Chat, Message
from .mixins import ChatExistsMixin, SeenMessageView


class ChatListView(LoginRequiredMixin, ListView):
    '''List of a users chats'''

    template_name = "chats/chat-list.html"
    context_object_name = 'chats'
    
    def get_queryset(self):
        return self.request.user.chats.all()

class ChatCreateView(LoginRequiredMixin, ChatExistsMixin, View):

    def get(self, request, *args, **kwargs):
        chat = Chat.objects.create()
        chat.participants.set([self.request.user, self.kwargs['participant_id']])
        messages.success(request, 'Chat created successfully', 'success')
        return redirect('chats:chat-detail', id=chat.id, code=chat.code)


class ChatDetailView(LoginRequiredMixin, SeenMessageView, ListView):
    '''Page of a chat that user can send, read a message'''

    template_name = 'chats/chat-detail.html'
    context_object_name = 'all_messages'

    def get_queryset(self):
        _from = self.request.GET.get('from')
        to = self.request.GET.get('to')
        if _from and to:
            return self.chat.messages.all().order_by("-date")[int(_from):int(to)][:20]

        return self.chat.messages.all().order_by("-date")[:20]
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['chat_id'] = self.chat.id
        context['chat_code'] = self.chat.code
        return context