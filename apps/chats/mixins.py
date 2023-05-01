from accounts.models import Account
from django.shortcuts import get_object_or_404, redirect


class ChatExistsMixin():
    '''Check if a chat exists and user is a participant of that'''

    def dispatch(self, request, *args, **kwargs):

        participant_ids = [request.user.id, self.kwargs['participant_id']]

        self.chat = self.request.user.chats.filter(participants__id__in=participant_ids).first()

        if self.chat:
            return redirect('chats:chat-detail', id=self.chat.id, code=self.chat.code)

        return super().dispatch(request, *args, **kwargs)
