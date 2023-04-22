from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, View, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.template.defaultfilters import slugify
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q


from products.models import  Category, Product
from customer.models import Order
from .forms import ProductForm


class AddProduct(LoginRequiredMixin, CreateView):
    '''Simply add a product'''

    form_class = ProductForm
    template_name = 'products/add-product.html'

    @transaction.atomic
    def form_valid(self, form):
        # TODO add this page later
        pass
        # form = self.form_class(self.request.POST, self.request.FILES)
        # data = form.save(commit=False)
        # cd = form.cleaned_data

        # data.seller = self.request.user
        # data.slug = slugify(data.title)

        # ship_from = cd["shipping_from_country"]
        # ship_to = cd["shipping_to_country"]

        # data.shipping_from, i = Country.objects.get_or_create(name=ship_from, slug=slugify(ship_from))
        # data.shipping_to, i = Country.objects.get_or_create(name=ship_to, slug=slugify(ship_to))

        # # Check if a user selected an existing category
        # if (cat := cd["child_category"]):
        #     data.category= cat

        # # if not create a category
        # elif (category := cd["child_category_create"]):
        #         if (parent:= cd["parent_category"]):
        #             data.category, i = Category.objects.get_or_create(parent=parent, title= category,
        #                                                               slug= slugify(category))
        #         elif (parent:= cd["parent_category_create"]):
        #             parent_cat, i = Category.objects.get_or_create(title=parent, slug=slugify(parent))
        #             data.category, i = Category.objects.get_or_create(parent=parent_cat, title=category,
        #                                                               slug=slugify(category))

        # form.save()
        # messages.success(self.request, "Item added successfully.", "success")
        # return redirect("products:list-product")

    def form_invalid(self, form):
        messages.success(self.request, "There was an error while saving your information", "success")
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


class UserProduct(LoginRequiredMixin, ListView):
    '''Show all registered products of a user'''

    template_name = "products/user-products.html"
    context_object_name = "products"

    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user)
