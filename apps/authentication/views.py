from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import F

from authentication.models import Account, VendorRate


class Profile(DetailView):
    '''A simple profile page for users'''

    template_name = "authentication/profile.html"
    context_object_name = "user"

    def get_object(self):
        return get_object_or_404(Account, id=self.kwargs['id'], token=self.kwargs["token"])

    def get_context_data(self, **kwargs):
        context = super(Profile, self).get_context_data(**kwargs)
        # get values of all votes related to a user
        rate = self.get_object().likes.values("vote")

        context['likes'] = rate.filter(vote="l").count()
        context['dislikes'] = rate.filter(vote="d").count()

        return context


class Like(LoginRequiredMixin, View):
    '''Like a user'''
    def get(self, request, id, token):
        vendor = get_object_or_404(Account, id= id, token= token)

        if vendor == self.request.user:
            messages.success(self.request, "You cant rate yourself.", "danger")
            return redirect("authentication:profile", id=id, token=token)

        if not self.request.user.customer_rate.filter(vendor=vendor):
            VendorRate.objects.create(customer= self.request.user, vendor= vendor, vote="l")
            messages.success(self.request, "You have liked this user.", "success")
            return redirect("authentication:profile", id=id, token=token)

        messages.success(self.request, "You have already rated this user.", "warning")
        return redirect("authentication:profile", id=id, token=token)


class DisLike(LoginRequiredMixin, View):
    '''DisLike a user'''
    def get(self, request, id, token):
        vendor = get_object_or_404(Account, id= id, token= token)

        if vendor == self.request.user:
            messages.success(self.request, "You cant rate yourself.", "danger")
            return redirect("authentication:profile", id=id, token=token)

        if not self.request.user.customer_rate.filter(vendor=vendor):
            VendorRate.objects.create(customer= self.request.user, vendor= vendor, vote="d")
            messages.success(self.request, "You have disliked this user.", "success")
            return redirect("authentication:profile", id=id, token=token)

        messages.success(self.request, "You have already rated this user.", "warning")
        return redirect("authentication:profile", id=id, token=token)


class Exchange(LoginRequiredMixin, View):
    '''
        This page gives user 20 coin.
        you should add payment methods here
    '''
    def get(self, request):
        self.request.user.balance = self.request.user.balance + 20
        self.request.user.save()
        return render(self.request, "authentication/exchange.html")
