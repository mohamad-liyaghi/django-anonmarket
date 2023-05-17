from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404
from django.http import Http404
from accounts.models import Account
from chats.models import Chat

class ChatExistsMixin():
    '''Check if a chat exists and user is a participant of that'''

    def dispatch(self, request, *args, **kwargs):
        self.participant = get_object_or_404(Account, id=self.kwargs['participant_id'])
        participant_ids = [request.user.id, self.participant.id]

        self.chat = self.request.user.chats.filter(participants__id__in=participant_ids).first()

        if self.chat:
            return redirect('chats:chat-detail', id=self.chat.id, code=self.chat.code)

        return super().dispatch(request, *args, **kwargs)


class SeenMessageView:
    def dispatch(self, request, *args, **kwargs):
        
        self.chat = get_object_or_404(Chat, id=self.kwargs['id'], code=self.kwargs['code'])

        if not self.chat.participants.filter(id=self.request.user.id).exists():
            raise Http404("Chat does not exist or is not accessible")

        self.chat.messages.filter(~Q(sender=self.request.user)
                                        & Q(is_seen=False)).update(is_seen=True)

        self.chat.notifications.filter(account=request.user, is_active=True).update(is_active=False)
        return super().dispatch(request, *args, **kwargs)