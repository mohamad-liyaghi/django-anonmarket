from django.views.generic import UpdateView, DeleteView, DetailView, ListView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy

from products.models import  Product
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
        return redirect("products:product-list")


    def form_invalid(self, form):
        messages.success(self.request, "Invalid information were given.", "danger")
        return redirect("products:product-list")

class ProductDetailView(DetailView):
    '''Return detail of a product'''

    template_name = "products/product-detail.html"
    context_object_name = "product"

    def get_object(self):
        return get_object_or_404(Product, id=self.kwargs["id"], slug=self.kwargs["slug"])


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    '''Update page of a product'''

    template_name = "products/update-product.html"
    fields = ["title", "description", "picture", "shipping_origin",
              "shipping_destinations", "price", "is_available"]
    context_object_name = "product"

    def get_object(self):
        return get_object_or_404(Product, id=self.kwargs["id"],
                                 slug=self.kwargs["slug"],
                                 provider=self.request.user)
    
    def get_success_url(self):
        return reverse_lazy("products:product-detail",
                             kwargs={"id": self.kwargs["id"],
                                     "slug": self.kwargs["slug"]})
    

class ProductDeleteView(LoginRequiredMixin, DeleteView):
    '''Delete a product by its provider'''

    template_name = "products/delete-product.html"
    context_object_name = "product"
    success_url = reverse_lazy("products:product-list")

    def get_object(self):
        return get_object_or_404(Product, id=self.kwargs["id"],
                                 slug=self.kwargs["slug"],
                                 provider=self.request.user)
