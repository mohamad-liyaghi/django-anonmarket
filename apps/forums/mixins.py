from django.shortcuts import get_object_or_404
from forums.models import Forum


class ForumObject:
    def dispatch(self, request, *args, **kwargs):
        self.forum = get_object_or_404(Forum, id=self.kwargs['id'], slug=self.kwargs['slug'])
        return super().dispatch(request, *args, **kwargs)