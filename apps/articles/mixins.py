from django.shortcuts import redirect

class ArticleAccessMixin:
    """
    Mixin to check article access for logged in users
    """
    def dispatch(self, request, *args, **kwargs):
        article = self.get_object()
        user = request.user

        if article.price == 0 or request.user == article.author or user.article_purchases.filter(article=article).exists():
            return super().dispatch(request, *args, **kwargs)
        
        return redirect('article:purchase-article')