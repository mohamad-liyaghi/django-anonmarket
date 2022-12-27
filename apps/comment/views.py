from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from comment.models import Comment


def is_ajax(request):
    '''Check if a request is ajax or not'''
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


class AddCommentView(LoginRequiredMixin, View):
    '''Add a comment for an object'''

    def get(self, request):
        return redirect("customer:home")

    def post(self, request):
        if is_ajax(request):

            # check if object_id and content_type and comment content exists
            if (object_id:=request.POST.get('object_id')) and \
                (content_type_id:=request.POST.get('content_type_id')) and \
                    (content:=request.POST.get('content')): 
                
                    content_type_model = get_object_or_404(ContentType, id=content_type_id)
                    object = get_object_or_404(content_type_model.model_class(), id=object_id)

                    #TODO create limitation for adding comments
                    comment = Comment.objects.create(user=request.user, content=content, 
                                    content_object= object)


            return JsonResponse({'error':'invalid information'})    

        return redirect("customer:home")