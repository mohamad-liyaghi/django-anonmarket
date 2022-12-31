from django.views.generic import FormView, DeleteView, DetailView, View, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template import RequestContext
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q, Count
from django.contrib import messages
from django.urls import reverse_lazy

import random

from customer.forms import OrderForm
from vendor.models import Product, Category
from customer.models import Order


class AddOrder(LoginRequiredMixin, FormView):
    '''Add an order'''

    template_name = "customer/add-order.html"
    form_class = OrderForm

    def dispatch(self, request, *args, **kwargs):
        """Check if object exist and has an appropriate customer"""

        # Get the available item
        self.object = get_object_or_404(Product, Q(id=kwargs["id"]) & Q(slug=kwargs["slug"])
                                        & Q(is_available=True))

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


class DeleteOrder(LoginRequiredMixin, DeleteView):
    '''Delete orders that vendor have not seen them'''

    template_name = "customer/delete-order.html"
    context_object_name = "order"

    def get_object(self):
        return get_object_or_404(Order, Q(id=self.kwargs["id"]) & Q(code=self.kwargs["code"])
                                        & Q(status="o") & Q(customer=self.request.user))

    def get_success_url(self):
        return reverse_lazy("vendor:product-detail", args = (self.get_object().item.pk, self.get_object().item.slug))


class OrderDetail(LoginRequiredMixin, DetailView):
    '''Show orders description (address) for vendor'''

    template_name = "customer/order-detail.html"
    context_object_name = "order"

    def get_object(self):
        return  get_object_or_404(Order, Q(id=self.kwargs["id"]) & Q(code=self.kwargs["code"])
                          & Q(item__seller=self.request.user))


class PayOrder(LoginRequiredMixin, View):
    '''Pay for an order'''

    def get(self, request, id, code):
        order = get_object_or_404(Order, id=id, code=code, customer=self.request.user, status="a")

        # check if user has enough money
        if self.request.user.balance >= order.price:
            self.request.user.balance = self.request.user.balance - order.price
            order.item.seller.balance = order.item.seller.balance + order.price
            order.status = "p"

            order.item.seller.save()
            self.request.user.save()
            order.save()
            messages.success(self.request, "order is paid now, wait for vendor to send the product.", "success")
            return redirect("customer:cart")

        messages.success(self.request, "You dont have money to pay for this order", "danger")
        return redirect("customer:cart")


class Cart(LoginRequiredMixin, ListView):
    '''Show a users orders'''

    template_name = "customer/cart.html"
    context_object_name = "orders"

    def get_queryset(self):
        return self.request.user.orders.all()


class Home(ListView):
    '''The main page that shows 20 most popular products'''

    template_name = "customer/home.html"
    context_object_name = "products"


    def get_queryset(self):
        # top 30 items
        return Product.objects.order_by("-vote")[:30]

class ProductSearch(ListView):
    '''Result of searchs'''

    template_name = "customer/product-search.html"
    context_object_name = "products"

    def get_queryset(self):
        q = self.request.GET.get('q')

        if q:
            return Product.objects.filter(
                Q(title__icontains=q) | Q(category__title=q)
            ).order_by("-is_available")

        return None


class FilterCategory(ListView):
    '''Show all products with the filtered category'''

    template_name = "customer/product-search.html"
    context_object_name = "products"

    def get_queryset(self):
        return Product.objects.filter(category__id=self.kwargs["id"],
                                      category__slug=self.kwargs["slug"])

# error handling functions
def handler404(request, exception):
    return render(request, "base/error/404.html")

def handler500(request, *args, **argv):
    return render(request, "base/error/500.html")