from django.views.generic import FormView, UpdateView, DeleteView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Count
from django.shortcuts import redirect, get_object_or_404
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

class ForumDetailView(LoginRequiredMixin, DetailView):
    '''Detail page of forum'''

    template_name = "forums/forum-detail.html"

    def get_object(self):
        return get_object_or_404(Forum, id=self.kwargs['id'], slug=self.kwargs['slug'])
    
    # TODO add top answers


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


class ForumDeleteView(LoginRequiredMixin, DeleteView):
    '''Delete a forum'''
    template_name = "forums/delete-forum.html"

    def get_object(self):
        k = self.kwargs
        return get_object_or_404(Forum, id=k["id"], slug=k["slug"],
                                 author=self.request.user)

    def get_success_url(self):
        return reverse_lazy("forums:forum-list")
