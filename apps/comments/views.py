from django.views.generic import View, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse_lazy
from django.contrib import messages
from comments.models import Comment
from comments.mixins import ObjectMixin

def is_ajax(request):
    '''Check if a request is ajax or not'''
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


class AddCommentView(LoginRequiredMixin, View):
    '''Add a comment for an object'''

    def get(self, request):
        return redirect("product-list")

    def post(self, request):
        if not is_ajax(request):
            return redirect("product-list")

        object_id = request.POST.get('object_id')
        content_type_id = request.POST.get('content_type_id')
        body = request.POST.get('body')

        if not all([object_id, content_type_id, body]):
            return JsonResponse({'error': 'invalid information'})

        content_type = get_object_or_404(ContentType, id=content_type_id)
        obj = get_object_or_404(content_type.model_class(), id=object_id)

        comment = Comment.objects.create(
            user=request.user,
            body=body,
            content_object=obj
        )

        response_data = {
            'created': {
                'user': comment.user.username,
                'body': comment.body,
                'date': comment.date
            }
        }

        return JsonResponse(response_data)
    
class CommentListView(ObjectMixin, ListView):
    template_name = 'comments/comment-list.html'
    context_object_name = 'comments'

    def get_queryset(self):
        return self.object.comments.all().order_by('-is_pinned')


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    '''Update a comment by its writer'''

    template_name = 'comments/update-comment.html'
    fields = ['body']

    def get_object(self):
        return get_object_or_404(Comment, id=self.kwargs['comment_id'], user=self.request.user)
    
    def get_success_url(self) -> str:
        return reverse_lazy("comments:comment-detail", kwargs={"id" : self.kwargs["comment_id"]})
    
    def post(self, request, *args, **kwargs):
            messages.success(request, 'Comment updated.', 'success')
            return super().post(request, *args, **kwargs)

    

class CommentDeleteView(LoginRequiredMixin, DeleteView):
        template_name = 'comments/delete-comment.html'
        success_url = '/'

        def get_object(self):
            return get_object_or_404(Comment, id=self.kwargs['comment_id'], user=self.request.user)
        
        def post(self, request, *args, **kwargs):
            messages.success(request, 'Comment deleted.', 'danger')
            return super().post(request, *args, **kwargs)