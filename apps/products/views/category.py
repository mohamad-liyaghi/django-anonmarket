from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from products.models import Product
from products.forms import CategoryForm


class ProductCategoryView(LoginRequiredMixin, View):
    '''List of a products categories and add/remove an item.'''
    
    template_name = 'category/product-category.html'
    
    def get_object(self):
        return get_object_or_404(Product, provider=self.request.user, id=self.kwargs['id'], slug=self.kwargs['slug'])

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        return render(request, self.template_name, {'object_category' : obj.category, 'form' : CategoryForm()})

    def post(self, request, *args, **kwargs):
        obj = self.get_object()

        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(instance=obj)
            messages.success(request, 'Category added for item.', 'success')
            return redirect('products:product-detail', id=obj.id, slug=obj.slug)
        
        messages.success(request, 'Invalid information.', 'danger')
        return redirect('products:product-detail', id=obj.id, slug=obj.slug)
