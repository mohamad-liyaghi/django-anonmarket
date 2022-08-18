from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from authentication.models import Account


class Profile(DetailView):
    '''A simple profile page for users'''

    template_name = "authentication/profile.html"
    context_object_name = "user"

    def get_object(self):
        return get_object_or_404(Account, id=self.kwargs['id'], token=self.kwargs["token"])
