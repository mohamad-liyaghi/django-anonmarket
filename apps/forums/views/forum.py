from django.views.generic import FormView, UpdateView, DeleteView, View, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.defaultfilters import slugify
from django.contrib import messages
from django.db.models import Q, Count
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy

from ..forms import ForumForm
from forums.models import Forum
from accounts.models import Account


class ForumListView(LoginRequiredMixin, ListView):
    '''Show all newest forums'''
    template_name = "forums/forum-list.html"
    context_object_name = "forums"

    def get_queryset(self):
        forums = None
        user_token = self.request.GET.get('user')
        latest = self.request.GET.get('latest')
        title = self.request.GET.get('title')

        if user_token:
            # Get a users Forums
            user = get_object_or_404(Account, token=user_token)
            forums = user.forums.all()
        
        if latest:
            forums = Forum.objects.all().order_by('-date')

        # Filter article by its title
        if title:
            forums = Forum.objects.filter(title__icontains=title)

        else:
            forums = Forum.objects.all().annotate(
                vote_count=Count('votes')
            ).order_by('-vote_count')


        return forums.order_by('-closed')[:20]


class ForumCreateView(LoginRequiredMixin, FormView):
    '''Create a new forum'''

    template_name = "forums/create-forum.html"
    form_class = ForumForm

    def form_valid(self, form):
        forum = form.save(commit=True, author=self.request.user)
        messages.success(self.request, 'Forum Created!', 'suceess')
        return redirect('forums:forum-detail', id=forum.id, slug=forum.slug)

    def form_invalid(self, form):
        messages.success(self.request, "Invalid information, try again.", "danger")
        return redirect("forums:create-forum")


class ForumUpdateView(LoginRequiredMixin, UpdateView):
    '''Update a forum (close or change price)'''

    template_name = "forums/update-forum.html"
    fields = ["title", "body", "closed"]

    def get_object(self):
        return get_object_or_404(Forum, id=self.kwargs["id"], slug=self.kwargs["slug"],
                                 author=self.request.user)

    def get_success_url(self):
        return reverse_lazy("forums:forum-detail", kwargs={"id": self.kwargs["id"],"slug": self.kwargs["slug"]})


class DeleteForum(LoginRequiredMixin, DeleteView):
    '''Delete a forum'''
    template_name = "forum/delete-forum.html"

    def get_object(self):
        k = self.kwargs
        return get_object_or_404(Forum, id=k["id"], slug=k["slug"],
                                 author=self.request.user)

    def get_success_url(self):
        return reverse_lazy("forums:user-forums")


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

            return redirect("forums:buy-forum", self.object.id, self.object.slug)

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
                return redirect("forums:forum-detail", id=self.kwargs["id"], slug=self.kwargs["slug"])

            messages.success(self.request, "You dont have enough money :(", "danger")
            return redirect("forums:forum-list")

        messages.success(self.request, "You have already bought this item", "warning")
        return redirect("forums:forum-detail", id=self.kwargs["id"], slug=self.kwargs["slug"])