from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, View, ListView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q


from products.models import  Category, Product
from customer.models import Order
from ..forms import ProductForm


class ProductListView(LoginRequiredMixin, ListView):
    '''Show all products, if there is any param given, give the users products'''

    template_name = "products/list-product.html"
    context_object_name = "products"

    def get_queryset(self):
        # If user is given, return users products, othervise return all products
        if (username:=self.request.GET.get('username')):
            return Product.objects.filter(provider__username=username).order_by('-is_available')
        
        return Product.objects.all()


class ProductCreateView(LoginRequiredMixin, FormView):
    '''A view for creating products'''

    form_class = ProductForm
    template_name = 'products/create-product.html'

    def form_valid(self, form):
        form = self.form_class(self.request.POST, self.request.FILES)
        data = form.save(commit=False)
        data.provider = self.request.user
        data.save()
        messages.success(self.request, "Product added successfully.", "success")
        return redirect("products:list-product")


    def form_invalid(self, form):
        messages.success(self.request, "Invalid information were given.", "danger")
        return redirect("products:list-product")


class UpdateProduct(LoginRequiredMixin, UpdateView):
    '''Update a products status or price'''

    template_name = "products/update-product.html"
    fields = ["price", "is_available"]
    context_object_name = "product"

    def get_object(self):
        return get_object_or_404(Product, id= self.kwargs["id"], slug= self.kwargs["slug"], seller=self.request.user)


class DeleteProduct(LoginRequiredMixin, DeleteView):
    '''Delete a Product'''

    template_name = "products/delete-product.html"
    context_object_name = "product"

    def get_object(self):
        return get_object_or_404(Product, id= self.kwargs["id"], slug= self.kwargs["slug"], seller=self.request.user)


class ProductDetail(DetailView):
    '''Return detail of a product'''

    template_name = "products/product-detail.html"
    context_object_name = "product"

    def get_object(self):
        return get_object_or_404(Product, id=self.kwargs["id"], slug=self.kwargs["slug"])


class AcceptOrder(LoginRequiredMixin, View):
    '''Accept a User Order'''

    def get(self, request, id, code):
        object = get_object_or_404(Order, id=id, code=code,
                                    item__seller=self.request.user, status="o")
        object.status = "a"
        object.save()

        messages.success(self.request, "Order accepted, wait for payment.", "success")
        return redirect("products:order-list")


class RejectOrder(LoginRequiredMixin, View):
    '''Reject a User Order'''

    def get(self, request, id, code):
        object = get_object_or_404(Order, id=id, code=code,
                                    item__seller=self.request.user, status="o")
        object.status = "r"
        object.save()

        messages.success(self.request, "Order rejected.", "danger")
        return redirect("products:order-list")


class OrderList(LoginRequiredMixin, ListView):
    '''List of all orders'''

    template_name = "products/order-list.html"
    context_object_name = "orders"

    def get_queryset(self):
        return Order.objects.filter(Q(item__seller=self.request.user) & ~Q(status="r"))


class SendOrder(LoginRequiredMixin, View):
    '''Change Order status to "send" '''

    def get(self, request, id, code):
        object = get_object_or_404(Order, id=id, code=code,
                                    item__seller=self.request.user, status="p")
        object.status = "s"
        object.save()

        messages.success(self.request, "Order Sent.", "success")
        return redirect("products:order-list")


