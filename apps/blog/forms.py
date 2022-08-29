from django import forms
from vendor.models import Product
from blog.models import Article, ArticleComment


class ArticleForm(forms.ModelForm):
    '''A form for creating articles'''

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.fields["product"].queryset = Product.objects.filter(seller=self.request.user)

    class Meta:
        model = Article
        fields = ("title", "body", "product", "price", "published", "allowed_members")


class CommentForm(forms.ModelForm):
    class Meta:
        model = ArticleComment
        fields = ("article", "body", "user")