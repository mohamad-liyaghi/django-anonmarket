from django.views.generic import View, UpdateView, DeleteView
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.defaultfilters import slugify
from django.contrib import messages
from django.urls import reverse_lazy

from blog.forms import ArticleForm
from blog.models import Article



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
            return redirect("blog:article-list")

        messages.success(self.request, "Sth went wrong with your information", "success")
        return redirect("blog:article-list")


class UpdateArticle(LoginRequiredMixin, UpdateView):
    '''Update an article'''

    template_name = "blog/update-article.html"
    fields = ["title", "body", "price", "published"]


    def get_object(self):
        return get_object_or_404(Article, id=self.kwargs["id"], slug=self.kwargs["slug"],
                                 author= self.request.user)


    def get_success_url(self):
        return redirect("blog:article-detail", id=self.kwargs["id"], slug=self.kwargs["slug"])



class DeleteArticle(LoginRequiredMixin, DeleteView):
    """Delete an article"""

    template_name = "blog/delete-article.html"
    success_url = reverse_lazy("blog:article-list")


    def get_object(self):
        return get_object_or_404(Article, id=self.kwargs["id"], slug=self.kwargs["slug"],
                                 author= self.request.user)