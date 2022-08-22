from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class ChatList(LoginRequiredMixin, TemplateView):
    '''Show All Available chats of a user'''
    template_name = "message/chat-list.html"


    def get_context_data(self, **kwargs):
        context = super(ChatList, self).get_context_data(**kwargs)

        context['creator_chats'] = self.request.user.chat_member.all()
        context['member_chats'] = self.request.user.chat_creator.all()


        return context
