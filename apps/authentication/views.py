from django.shortcuts import get_object_or_404, redirect
from django.views.generic import View, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from authentication.models import Account, Rate


class Profile(DetailView):
    '''A simple profile page for users'''

    template_name = "authentication/profile.html"
    context_object_name = "user"

    def get_object(self):
        return get_object_or_404(Account, id=self.kwargs['id'], token=self.kwargs["token"])


class Like(LoginRequiredMixin, View):
    '''Like a user'''
    def get(self, request, id, token):
        vendor = get_object_or_404(Account, id= id, token= token)

        if vendor == self.request.user:
            messages.success(self.request, "You cant rate yourself.", "danger")
            return redirect("authentication:profile", id=id, token=token)

        if not self.request.user.customer_rate.filter(vendor=vendor):
            Rate.objects.create(customer= self.request.user, vendor= vendor, vote="l")
            messages.success(self.request, "You have liked this user.", "success")
            return redirect("authentication:profile", id=id, token=token)

        messages.success(self.request, "You have already liked this user.", "warning")
        return redirect("authentication:profile", id=id, token=token)
