from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404


class ChatExistsMixin():
    '''Check if a chat exists and user is a participant of that'''

    def dispatch(self, request, *args, **kwargs):

        participant_ids = [request.user.id, self.kwargs['participant_id']]

        self.chat = self.request.user.chats.filter(participants__id__in=participant_ids).first()

        if self.chat:
            return redirect('chats:chat-detail', id=self.chat.id, code=self.chat.code)

        return super().dispatch(request, *args, **kwargs)


class SeenMessageView:
    def dispatch(self, request, *args, **kwargs):
        self.chat = get_object_or_404(self.request.user.chats.all(), id=self.kwargs['id'], code=self.kwargs['code'])

        self.chat.messages.filter(~Q(sender=self.request.user)
                                        & Q(is_seen=False)).update(is_seen=True)

        return super().dispatch(request, *args, **kwargs)