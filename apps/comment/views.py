from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from comment.models import Comment
import datetime


def is_ajax(request):
    '''Check if a request is ajax or not'''
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


class AddCommentView(LoginRequiredMixin, View):
    '''Add a comment for an object'''

    def get(self, request):
        return redirect("product-list")

    def post(self, request):
        if is_ajax(request):

            # check if object_id and content_type and comment content exists
            if (object_id:=request.POST.get('object_id')) and \
                (content_type_id:=request.POST.get('content_type_id')) and \
                    (content:=request.POST.get('content')): 
                
                    content_type_model = get_object_or_404(ContentType, id=content_type_id)
                    object = get_object_or_404(content_type_model.model_class(), id=object_id)

                    time = datetime.datetime.now() - datetime.timedelta(minutes=5)

                    if Comment.objects.filter(user=self.request.user, date__gte=time).count() <= 5:
                        Comment.objects.create(user=request.user, content=content, 
                                        content_object= object)
                        return JsonResponse({'created':'Comment created'})                                                    

                    return JsonResponse({'limit-error':'more than 5 comments in 5 mins is not allowed'})            


            return JsonResponse({'error':'invalid information'})    

        return redirect("product-list")



class CommentDeleteView(LoginRequiredMixin, View):
    def get(self, request):
        return redirect("orders:")

    def post(self, request):
        if is_ajax(request):
            # check if object_id and content_type and comment content exists
            if (object_id:=request.POST.get('object_id')) and \
                (content_type_id:=request.POST.get('content_type_id')) and \
                    (comment_id:=request.POST.get('comment_id')): 
                
                    content_type_model = get_object_or_404(ContentType, id=content_type_id)
                    object = get_object_or_404(content_type_model.model_class(), id=object_id)
                    comment = object.comment.filter(user=self.request.user, id=comment_id)

                    if comment:
                        comment.first().delete()
                        return JsonResponse({'deleted':'Comment deleted'})                      

                    return JsonResponse({'not found':'Comment does not found'})


            return JsonResponse({'error':'invalid information'})    

        return redirect("product-list")