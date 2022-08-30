from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.defaultfilters import slugify
from django.contrib import messages
from django.shortcuts import redirect

from .forms import ForumForm


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




