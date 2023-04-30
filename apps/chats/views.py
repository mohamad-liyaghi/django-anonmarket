from django.views.generic import ListView, View, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.db.models import Q 

import random

from accounts.models import Account
from chats.models import Chat, Message
from .forms import MessageForm


class ChatListView(LoginRequiredMixin, ListView):
    '''List of a users chats'''

    template_name = "chats/chat-list.html"
    context_object_name = 'chats'
    
    def get_queryset(self):
        return self.request.user.chats.all()


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
        return redirect("chats:chat-detail", existing_chat.pk, existing_chat.code)



class ChatDetail(LoginRequiredMixin, View):
    '''Page of a chat that user can send, read a message'''

    def setup(self, request, *args, **kwargs):
        '''Get The chat'''
        self.chat = get_object_or_404(Chat, Q(id= kwargs["id"]) & Q(code=kwargs["code"]) & Q(creator=request.user)
                                      | Q(member=request.user) & Q(id= kwargs["id"]) & Q(code=kwargs["code"]))

        return super().setup(request, *args, **kwargs)


    def get(self, request, id, code):
        """Return the messages of a chat"""

        messages = self.chat.chats.all().order_by("-date")

        # seen messages
        messages.filter(~Q(sender=self.request.user)
                                        & Q(is_seen=False)).update(is_seen=True)

        form = MessageForm

        return render(self.request, "message/chat-detail.html",
                      {"all_messages" : messages[:50], "chat" : self.chat, "form" : form})


    def post(self, request, *args, **kwargs):
        '''Create a message in chat'''

        form = MessageForm(self.request.POST)

        if form.is_valid():
            form = form.save(commit=False)
            form.chat = self.chat
            form.sender = self.request.user
            form.save()

        return redirect("chats:chat-detail", self.chat.pk, self.chat.code)


class UpdateMessage(LoginRequiredMixin, UpdateView):
    '''Update a message by its sender'''

    template_name = "message/update-message.html"
    context_object_name = "message"
    fields = ["text"]

    def get_object(self):
        return get_object_or_404(Message, Q(id=self.kwargs["id"])
                                 & Q(sender=self.request.user) & ~Q(is_seen=True))

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.is_edited = True
        instance.save()
        return redirect("chats:chat-detail", self.get_object().chat.id, self.get_object().chat.code)


class DeleteMessage(DeleteView):
    '''Delete a Message'''

    template_name = "message/delete-message.html"

    def get_object(self):
        return get_object_or_404(Message, Q(id=self.kwargs["id"])
                                 & Q(sender=self.request.user) & ~Q(is_seen=True))

    def get_success_url(self):
        return reverse_lazy("chats:chat-detail",
                            args=(self.get_object().chat.id, self.get_object().chat.code))

