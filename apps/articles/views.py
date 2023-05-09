from django.views.generic import View, UpdateView, DeleteView, DetailView, ListView
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.defaultfilters import slugify
from django.contrib import messages
from django.db.models import Q, Count
from django.urls import reverse_lazy

from articles.forms import ArticleForm
from articles.models import Article
from accounts.models import Account
from products.models import Product


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

class CreateArticle(LoginRequiredMixin, View):
    '''Create an article'''

    template_name = "blog/create-article.html"
    form_class = ArticleForm


    def get(self, request):
        # Here we send request to the form for product filters
        form = self.form_class(request=request)
        return render(self.request, self.template_name, {"form" : form})


    def post(self, request):
        form = self.form_class(self.request.POST, request=self.request)

        if form.is_valid():
            data = form.save(commit=False)

            data.slug = slugify(data.title)
            data.author = self.request.user
            form.save()

            form.save_m2m()
            data.allowed_members.add(self.request.user.id)

            messages.success(self.request, "Article created", "success")
            return redirect("article:user-articles")

        messages.success(self.request, "Sth went wrong with your information", "success")
        return redirect("article:user-articles")


class UpdateArticle(LoginRequiredMixin, UpdateView):
    '''Update an article'''

    template_name = "blog/update-article.html"
    fields = ["title", "body", "price", "published"]


    def get_object(self):
        return get_object_or_404(Article, id=self.kwargs["id"], slug=self.kwargs["slug"],
                                 author= self.request.user)

    def get_success_url(self):
        return reverse_lazy("article:article-detail", kwargs={"id" : self.kwargs["id"], "slug" : self.kwargs["slug"]})


class DeleteArticle(LoginRequiredMixin, DeleteView):
    """Delete an article"""

    template_name = "blog/delete-article.html"
    success_url = reverse_lazy("article:user-articles")

    def get_object(self):
        return get_object_or_404(Article, id=self.kwargs["id"], slug=self.kwargs["slug"],
                                 author= self.request.user)


class ArticleDetail(LoginRequiredMixin, DetailView):
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


class PublishArticle(LoginRequiredMixin, View):
    '''Publish an article'''

    def get(self, request, *args,  **kwargs):

        object = get_object_or_404(Article, id=self.kwargs["id"], slug=self.kwargs["slug"],
                                   author= self.request.user, published=False)

        object.published = True
        object.save()
        messages.success(self.request, "Article published", "success")
        return redirect("article:article-detail", id=self.kwargs["id"], slug=self.kwargs["slug"])


class BuyArticle(LoginRequiredMixin, View):
    '''Buy an article'''

    def get(self, request, *args, **kwargs):
        object = get_object_or_404(Article, Q(id=self.kwargs["id" ]) & Q(slug=self.kwargs["slug"])
        & Q(published=True) & ~Q(price=0))
        return render(self.request, "blog/buy-article.html", {"article" : object})


    def post(self, request, *args, **kwargs):
        object = get_object_or_404(Article, Q(id=self.kwargs["id"]) & Q(slug=self.kwargs["slug"])
                                   & Q(published=True) & ~Q(price=0))
        if not self.request.user in object.allowed_members.all():
            if self.request.user.balance >= object.price:
                self.request.user.balance = self.request.user.balance - object.price
                object.author.balance = object.author.balance + object.price
                object.allowed_members.add(self.request.user)

                self.request.user.save()
                object.save()
                object.author.save()
                messages.success(self.request, "Article Purchased")
                return redirect("article:article-detail", id=self.kwargs["id"], slug=self.kwargs["slug"])

            messages.success(self.request, "You dont have enough money :(", "success")

        messages.success(self.request, "You have already bought this item", "success")
        return redirect("article:article-detail", id=self.kwargs["id"], slug=self.kwargs["slug"])


class UserArticleList(LoginRequiredMixin, ListView):
    '''Show all users articles'''

    template_name = "blog/article-list.html"
    context_object_name = "articles"

    def get_queryset(self):
        return Article.objects.filter(author=self.request.user)