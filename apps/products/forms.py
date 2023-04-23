from django import forms
from products.models import Product, Category

class ProductForm(forms.ModelForm):
    # # users can select the category from this list
    # child_category = forms.ModelChoiceField(queryset= Category.objects.filter(parent__isnull=False), required=False)

    # # this field are being used for creating categories
    # parent_category = forms.ModelChoiceField(queryset=Category.objects.filter(parent__isnull=True), required=False)
    # parent_category_create = forms.CharField(required=False)
    # child_category_create = forms.CharField(required=False)

    # # countries
    # shipping_from_country = forms.CharField(required=True)
    # shipping_to_country = forms.CharField(required=True)

    class Meta:
        model = Product
        fields = [
            'title',
            'description',
            'picture',
            'price',
            'shipping_origin',
            'shipping_destinations',
            'is_available',
            
        ]
