from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q
from django.contrib import messages

import random

from customer.forms import OrderForm
from vendor.models import Product
from customer.models import Order



class AddOrder(LoginRequiredMixin, FormView):
    '''Add an order'''

    template_name = "customer/add-order.html"
    form_class = OrderForm

    def dispatch(self, request, *args, **kwargs):
        """Check if object exist and has an appropriate customer"""

        # Get the available item
        self.object = get_object_or_404(Product, Q(id=kwargs["id"]) & Q(slug=kwargs["slug"]) & Q(is_available=True))

        # check if customer is not the items vendor
        if self.object.seller == self.request.user:
            messages.success(self.request, "You cant order your own products.", "danger")
            return redirect("vendor:product-detail", id=self.kwargs["id"], slug=self.kwargs["slug"])

        # check if customer hasnt ordered this before
        if Order.objects.filter(Q(item=self.object) & Q(customer=self.request.user) & Q(status="o")):
            messages.success(self.request, "You have already ordered this item, please wait for result.", "danger")
            return redirect("vendor:product-detail", id=self.kwargs["id"], slug=self.kwargs["slug"])

        return super().dispatch(request, *args, **kwargs)


    def form_valid(self, form):
        form = form.save(commit=False)

        form.code = random.randint(0, 99999999999999999999)
        form.item = self.object
        form.price = self.object.price
        form.customer = self.request.user
        form.save()

        messages.success(self.request, "Item ordered, wait for results.", "success")
        return redirect("vendor:product-detail", id=self.kwargs["id"], slug=self.kwargs["slug"])

    def form_invalid(self, form):
        messages.success(self.request, "Sth  went wrong with your information...", "danger")
        return redirect("vendor:product-detail", id=self.kwargs["id"], slug=self.kwargs["slug"])









