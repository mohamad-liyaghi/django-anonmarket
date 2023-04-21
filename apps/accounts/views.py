from django.shortcuts import get_object_or_404, render
from django.views.generic import View, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from accounts.models import Account


class ProfileView(DetailView):
    '''Users profile page'''

    template_name = "accounts/profile.html"
    context_object_name = "user"

    def get_object(self):
        return get_object_or_404(Account, id=self.kwargs['id'], token=self.kwargs["token"])

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        
        context['products'] = self.get_object().products.all().order_by("-vote")
        context["articles"] = self.get_object().articles.all().filter(published=True)[:5]

        return context


class ExchangeView(LoginRequiredMixin, View):
    '''
        This page gives user 20 coin.
        you should add payment methods here
    '''
    def get(self, request):
        self.request.user.balance = self.request.user.balance + 20
        self.request.user.save()
        return render(self.request, "accounts/exchange.html")
