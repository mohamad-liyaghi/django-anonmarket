from django.views.generic import FormView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.defaultfilters import slugify
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy

from .forms import ForumForm
from forum.models import Forum



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

        context = {"forum" : self.object}

        return render(self.request, self.template_name, context)
