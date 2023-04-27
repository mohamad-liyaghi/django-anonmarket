from django.views.generic import View, DeleteView, DetailView, ListView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from django.contrib import messages
from django.http import JsonResponse

from products.models import Product
from orders.models import Order

def is_ajax(request):
    '''Check if a request is ajax or not'''
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


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

        return redirect('products:order-list')




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
            return redirect("orders:cart")

        messages.success(self.request, "You dont have money to pay for this order", "danger")
        return redirect("orders:cart")


class Cart(LoginRequiredMixin, ListView):
    '''Show a users orders'''

    template_name = "orders/cart.html"
    context_object_name = "orders"

    def get_queryset(self):
        return self.request.user.orders.all()


class Home(ListView):
    '''The main page that shows 20 most popular products'''

    template_name = "orders/home.html"
    context_object_name = "products"


    def get_queryset(self):
        # top 30 items
        return Product.objects.order_by("-vote")[:30]

class ProductSearch(ListView):
    '''Result of searchs'''

    template_name = "orders/product-search.html"
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

    template_name = "orders/product-search.html"
    context_object_name = "products"

    def get_queryset(self):
        return Product.objects.filter(category__id=self.kwargs["id"],
                                      category__slug=self.kwargs["slug"])

# error handling functions
def handler404(request, exception):
    return render(request, "base/error/404.html")

def handler500(request, *args, **argv):
    return render(request, "base/error/500.html")