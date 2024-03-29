from django import forms
from products.models import Product
from articles.models import Article


class ArticleForm(forms.ModelForm):
    '''A form for creating articles'''

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.fields["product"].queryset = Product.objects.filter(provider=self.user)

    class Meta:
        model = Article
        fields = ["title", "body", "product", "price", "published"]


    def save(self, commit=True, author=None):
        article = super().save(commit=False)
        article.author = author
        article.save()
        return article