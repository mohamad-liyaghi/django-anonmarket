from django.views.generic import FormView, UpdateView, DeleteView, DetailView, ListView, CreateView
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Count
from django.urls import reverse_lazy, reverse

from articles.forms import ArticleForm
from articles.models import Article, ArticlePurchase
from accounts.models import Account
from products.models import Product
from articles.mixins import ArticleAccessMixin


class ArticleListView(LoginRequiredMixin, ListView):

    template_name = "articles/article-list.html"
    context_object_name = "articles"

    def get_queryset(self):
        articles = None

        user_token = self.request.GET.get('user')
        product_slug = self.request.GET.get('product')
        latest = self.request.GET.get('latest')
        title = self.request.GET.get('title')

        if user_token:
            user = get_object_or_404(Account, token=user_token)

            if user == self.request.user:
                articles = user.articles.all()
            else:
                articles = user.articles.filter(published=True)

            return articles
        
        # Filter a products articles
        if product_slug:
            product = get_object_or_404(Product, slug=product_slug)
            articles = product.articles.all()

        # Show latest articles
        if latest:
            articles = Article.objects.filter(published=True).order_by('-date')

        # Filter article by its title
        if title:
            articles = Article.objects.filter(published=True, title__icontains=title)

        else:
            # Show hot articles
            articles = Article.objects.filter(published=True).annotate(
                vote_count=Count('votes')
            ).order_by('-vote_count')

        return articles.order_by('-date')[:20]


class ArticleCreateView(LoginRequiredMixin, FormView):
    '''Create an article'''

    template_name = "articles/create-article.html"
    form_class = ArticleForm

    def form_valid(self, form):
        article = form.save(commit=True, author=self.request.user)
        messages.success(self.request, 'Article Created!', 'suceess')
        return redirect('article:article-detail', id=article.id, slug=article.slug)

    def form_invalid(self, form):
        messages.success(self.request, 'Invalid data...', 'danger')
        return redirect('article:article-list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

class UpdateArticle(LoginRequiredMixin, UpdateView):
    '''Update an article'''

    template_name = "articles/update-article.html"
    fields = ["title", "body", "price", "published"]


    def get_object(self):
        return get_object_or_404(Article, id=self.kwargs["id"], slug=self.kwargs["slug"],
                                 author=self.request.user)

    def get_success_url(self):
        return reverse_lazy("article:article-detail", kwargs={"id" : self.kwargs["id"], "slug" : self.kwargs["slug"]})


class DeleteArticle(LoginRequiredMixin, DeleteView):
    """Delete an article"""

    template_name = "articles/delete-article.html"
    success_url = reverse_lazy("article:article-list")

    def get_object(self):
        return get_object_or_404(Article, id=self.kwargs["id"], slug=self.kwargs["slug"],
                                 author= self.request.user)
    
    def post(self, request, *args, **kwargs):
        messages.success(request, 'Article deleted.', 'success')
        return super().post(request, *args, **kwargs)


class ArticleDetail(LoginRequiredMixin, ArticleAccessMixin, DetailView):
    """Detail page of an article"""

    template_name = "blog/article-detail.html"
    context_object_name = "article"

    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()

        if object.published:
            if object.price != 0:
                # check if user has permission
                if self.request.user in object.allowed_members.all():
                    return super().dispatch(request, *args, **kwargs)
                return redirect("article:buy-article", object.id, object.slug)

            # if blog is free
            return super().dispatch(request, *args, **kwargs)


        if object.author == self.request.user:
            return super().dispatch(request, *args, **kwargs)

        return redirect("article:article-list", object.id, object.slug)

    def get_object(self):
        return get_object_or_404(Article, id=self.kwargs["id"], slug=self.kwargs["slug"])


class ArticlePurchaseView(LoginRequiredMixin, CreateView):
    '''Purchase an article'''

    model = ArticlePurchase
    template_name = 'articles/purchase-article.html'
    context_object_name = 'article'
    fields = []

    def dispatch(self, request, *args, **kwargs):
        article = self.get_object()
        
        if article.price == 0 or request.user.article_purchases.filter(article=article).exists():
            messages.warning(request, 'You have already purchased this item.')
            return redirect('article:article-detail', id=article.id, slug=article.slug)
        
        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        return get_object_or_404(Article, id=self.kwargs["id"], slug=self.kwargs["slug"])

    def form_valid(self, form):
        article = self.get_object()
        form.instance.article = article
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        article = self.get_object()
        return reverse('article:article-detail', kwargs={'id': article.id, 'slug': article.slug})