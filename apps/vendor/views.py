from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.template.defaultfilters import slugify
from django.contrib import messages
from django.shortcuts import get_object_or_404


from vendor.models import Country, Category, Product
from .forms import ProductForm


class AddProduct(LoginRequiredMixin, CreateView):
    '''Simply add a product'''

    form_class = ProductForm
    template_name = 'vendor/add-product.html'

    @transaction.atomic
    def form_valid(self, form):
        form = self.form_class(self.request.POST, self.request.FILES)
        data = form.save(commit=False)
        cd = form.cleaned_data

        data.seller = self.request.user
        data.slug = slugify(data.title)

        ship_from = cd["shipping_from_country"]
        ship_to = cd["shipping_to_country"]

        data.shipping_from, i = Country.objects.get_or_create(name=ship_from, slug=slugify(ship_from))
        data.shipping_to, i = Country.objects.get_or_create(name=ship_to, slug=slugify(ship_to))

        # Check if a user selected an existing category
        if (cat := cd["child_category"]):
            data.category= cat

        # if not create a category
        elif (category := cd["child_category_create"]):
                if (parent:= cd["parent_category"]):
                    data.category, i = Category.objects.get_or_create(parent=parent, title= category,
                                                                      slug= slugify(category))
                elif (parent:= cd["parent_category_create"]):
                    parent_cat, i = Category.objects.get_or_create(title=parent, slug=slugify(parent))
                    data.category, i = Category.objects.get_or_create(parent=parent_cat, title=category,
                                                                      slug=slugify(category))

        form.save()
        messages.success(self.request, "Item added successfully.", "success")

    def form_invalid(self, form):
        messages.success(self.request, "There was an error while saving your information", "success")


class UpdateProduct(LoginRequiredMixin, UpdateView):
    '''Update a products status or price'''

    template_name = "vendor/update-product.html"
    fields = ["price", "is_available"]
    context_object_name = "product"

    def get_object(self):
        return get_object_or_404(Product, id= self.kwargs["id"], slug= self.kwargs["slug"], seller=self.request.user)

