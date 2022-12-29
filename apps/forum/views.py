from django.views.generic import FormView, UpdateView, DeleteView, View, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.defaultfilters import slugify
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy

from .forms import ForumForm
from forum.models import Forum


class ForumList(LoginRequiredMixin, ListView):
    '''Show all newest forums'''
    template_name = "forum/forum-list.html"
    context_object_name = "forums"

    def get_queryset(self):
        return Forum.objects.all().order_by("-date")[:20]


class UserForum(LoginRequiredMixin, ListView):
    '''Show all user forums'''
    template_name = "forum/forum-list.html"
    context_object_name = "forums"

    def get_queryset(self):
        return Forum.objects.filter(author=self.request.user)


class CreateForum(LoginRequiredMixin, FormView):
    '''Create a new forum'''

    template_name = "forum/create-forum.html"
    form_class = ForumForm

    def form_valid(self, form):
        form = self.form_class(self.request.POST)
        data = form.save(commit=False)

        data.slug = slugify(data.title)
        data.author = self.request.user

        form.save()
        form.save_m2m()

        data.allowed_members.add(self.request.user.id)
        messages.success(self.request, "Forum created successfully!", "success")
        return redirect("forum:user-forums")

    def form_invalid(self, form):
        messages.success(self.request, "Sth went wrong with your information.", "danger")
        return redirect("forum:user-forums")


class UpdateForum(LoginRequiredMixin, UpdateView):
    '''Update a forum (close or change price)'''

    template_name = "forum/update-forum.html"
    fields = ["price", "closed", "title", "body"]

    def get_object(self):
        k = self.kwargs

        return get_object_or_404(Forum, id=k["id"], slug=k["slug"],
                                 author=self.request.user)

    def get_success_url(self):
        return reverse_lazy("forum:user-forums")


class DeleteForum(LoginRequiredMixin, DeleteView):
    '''Delete a forum'''
    template_name = "forum/delete-forum.html"

    def get_object(self):
        k = self.kwargs
        return get_object_or_404(Forum, id=k["id"], slug=k["slug"],
                                 author=self.request.user)

    def get_success_url(self):
        return reverse_lazy("forum:user-forums")


class ForumDetail(LoginRequiredMixin, View):
    '''Detail page of forum and add comment'''

    template_name = "forum/forum-detail.html"

    def dispatch(self, request, *args, **kwargs):
        # get the object
        self.object = get_object_or_404(Forum, id=self.kwargs["id"],
                                   slug=self.kwargs["slug"])

        # check if object is free
        if self.object.price != 0:
            # check if user has permission to access forum
            if self.request.user in self.object.allowed_members.all():
                return super().dispatch(request, *args, **kwargs)

            return redirect("forum:buy-forum", self.object.id, self.object.slug)

        return super().dispatch(request, *args, **kwargs)


    def get(self, request, *args, **kwargs):

        context = {"forum" : self.object, "object" : self.object}
        return render(self.request, self.template_name, context)



class BuyForum(LoginRequiredMixin, View):
    '''Buy a forum in order to read comments'''

    def get(self, request, *args, **kwargs):
        object = get_object_or_404(Forum, Q(id=self.kwargs["id" ]) & Q(slug=self.kwargs["slug"])
        & ~Q(price=0))
        return render(self.request, "forum/buy-forum.html", {"forum" : object})

    def post(self, request, *args, **kwargs):
        object = get_object_or_404(Forum, Q(id=self.kwargs["id"]) & Q(slug=self.kwargs["slug"])
                                   & ~Q(price=0))

        if not self.request.user in object.allowed_members.all():
            if self.request.user.balance >= object.price:
                self.request.user.balance = self.request.user.balance - object.price
                object.author.balance = object.author.balance + object.price
                object.allowed_members.add(self.request.user)

                self.request.user.save()
                object.save()
                object.author.save()
                messages.success(self.request, "Forum Purchased")
                return redirect("forum:forum-detail", id=self.kwargs["id"], slug=self.kwargs["slug"])

            messages.success(self.request, "You dont have enough money :(", "danger")
            return redirect("forum:forum-list")

        messages.success(self.request, "You have already bought this item", "warning")
        return redirect("forum:forum-detail", id=self.kwargs["id"], slug=self.kwargs["slug"])

class ForumSearch(ListView):
    '''Result of search'''

    template_name = "forum/forum-list.html"
    context_object_name = "forums"

    def get_queryset(self):
        q = self.request.GET.get('q')

        if q:
            return Forum.objects.filter(
                Q(title__icontains=q) | Q(author__username=q)
            )

        return None