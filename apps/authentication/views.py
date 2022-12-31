from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from authentication.models import Account


class Profile(DetailView):
    '''A simple profile page for users'''

    template_name = "authentication/profile.html"
    context_object_name = "user"

    def get_object(self):
        return get_object_or_404(Account, id=self.kwargs['id'], token=self.kwargs["token"])

    def get_context_data(self, **kwargs):
        context = super(Profile, self).get_context_data(**kwargs)
        
        context['products'] = self.get_object().products.all().order_by("-vote")
        context["articles"] = self.get_object().articles.all().filter(published=True)[:5]

        return context


class Exchange(LoginRequiredMixin, View):
    '''
        This page gives user 20 coin.
        you should add payment methods here
    '''
    def get(self, request):
        self.request.user.balance = self.request.user.balance + 20
        self.request.user.save()
        return render(self.request, "authentication/exchange.html")
