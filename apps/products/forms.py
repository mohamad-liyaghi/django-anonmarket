from django import forms
from products.models import Product, Category

class ProductForm(forms.ModelForm):
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

class CategoryForm(forms.ModelForm):
    parent = forms.ModelChoiceField(queryset=Category.objects.filter(parent=None), required=False)
    class Meta:
        model = Category
        fields = ['title', 'parent']

    def save(self, instance):

        category = None

        if self.cleaned_data['title']:
            # get or create the category
            category, created = Category.objects.get_or_create(
                title=self.cleaned_data['title'].lower(), parent=self.cleaned_data['parent']
            )

        else:
            self.cleaned_data['parent']  = category

        # if category already is assigned to the object, it will remove it
        if category == instance.category:
            instance.category = None

        # othervise add the category for the object
        else:
            instance.category = category

        instance.save()


        
