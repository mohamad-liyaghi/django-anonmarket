from django.views.generic import View, DeleteView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from django.db import transaction
from django.contrib import messages
from django.http import JsonResponse

from products.models import Product
from orders.models import Order

def is_ajax(request):
    '''Check if a request is ajax or not'''
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


class OrderListView(LoginRequiredMixin, ListView):
    context_object_name = 'orders'

    def get_template_names(self):
        if self.request.GET.get('user', None) == 'me':
            return ['orders/order-list.html']
        else:
            return ['orders/customer-order-list.html']


    def get_queryset(self):
        if self.request.GET.get('user') == 'me':
            return Order.objects.filter(account=self.request.user)    
        
        return Order.objects.filter(provider=self.request.user).order_by('status')


class OrderCreateView(LoginRequiredMixin, View):
    """Create a new order with ajax"""

    def post(self, request, *args, **kwargs):
        if not is_ajax(request):
            return JsonResponse({"error": "This is not an ajax request."})

        object_id = request.POST.get("object_id")
        object_slug = request.POST.get("object_slug")
        quantity = request.POST.get("quantity")

        if not all([object_id, object_slug, quantity]):
            return JsonResponse({"error": "Information is incomplete."})

        description = request.POST.get("description", None)

        # Get the product that user wants to order
        product = get_object_or_404(Product, id=object_id, slug=object_slug)

        if not product.is_available:
            return JsonResponse({"error": "Product is not available."})

        # Update older order if there is one created
        order = Order.objects.filter(account=request.user, product=product, status="o").first()
        if order:
            order.description = description
            order.quantity = quantity
            order.save()
            return JsonResponse({"success": "An older order has been updated."})

        # Create a new order
        order = Order.objects.create(
            account=request.user,
            product=product,
            quantity=quantity,
            description=description,
            price=product.price,
        )

        return JsonResponse({"success": "Order has been created."})
        

class OrderStatusView(View):
    '''
    Accept/Reject an order
    Also change objects status to Shipped
    '''

    def get_object(self, id, token):
        return get_object_or_404(Order, id=id, token=token, product__provider=self.request.user)

    def get(self, request, id, token, status, *args, **kwargs):
        
        obj = self.get_object(id, token)

        if obj.status == 'o' and status in ['a', 'r']:
            obj.status = status
            obj.save()
            messages.success(request, f'Order request changed to {obj.get_status_display()}', 'success')

        elif obj.status == 'p' and status == 's':
            obj.status = status
            obj.save()
            messages.success(request, f'Order request changed to {obj.get_status_display()}', 'success')

        else:
            messages.error(request, 'Invalid status for this object.', 'danger')

        return redirect('orders:order-list')


class OrderDetail(LoginRequiredMixin, DetailView):
    '''Detail page of an order.'''

    template_name = "orders/order-detail.html"
    context_object_name = "order"

    def get_object(self):
        return get_object_or_404(Order, Q(id=self.kwargs["id"]) & Q(token=self.kwargs["token"]),
                                Q(account=self.request.user) | Q(product__provider=self.request.user))


class OrderDeleteView(LoginRequiredMixin, DeleteView):
    '''Delete orders that vendor have not seen them'''

    template_name = "orders/delete-order.html"
    context_object_name = "order"
    success_url = '/'

    def get_object(self):
        return get_object_or_404(Order, id=self.kwargs['id'], token=self.kwargs['token'],
                                account=self.request.user, status='o')


class OrderPayView(LoginRequiredMixin, View):
    """Pay for an order"""

    template_name = "orders/pay-order.html"

    def get_object(self, id, token):
        return get_object_or_404(
            Order,
            id=id,
            token=token,
            account=self.request.user,
            status="a",
            product__is_available=True,
        )

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object(
            self.kwargs["id"], self.kwargs["token"]
        )
        # redirect user to exchange page if user doesnt have enough money
        if request.user.balance < self.object.price:
            messages.success(
                self.request,
                "You dont have enough money, first charge your wallet.",
                "danger",
            )
            return redirect("accounts:exchange")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(
            request,
            self.template_name,
            {"order": self.get_object(self.kwargs["id"], self.kwargs["token"])},
        )

    @transaction.atomic
    def post(self, request, id, token):
        order = self.get_object(id, token)

        self.request.user.balance -= order.price
        order.product.provider.balance += order.price
        order.status = "p"
        order.is_paid = True

        order.product.provider.save()
        self.request.user.save()
        order.save()

        messages.success(
            self.request,
            "Order successfully got paid, want for provider to prepare it.",
            "success",
        )
        return redirect("orders:order-detail", id=order.id, token=order.token)


# error handling functions
def handler404(request, exception):
    return render(request, "base/error/404.html")

def handler500(request, *args, **argv):
    return render(request, "base/error/500.html")