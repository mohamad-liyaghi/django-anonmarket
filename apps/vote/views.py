from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

from django.contrib.contenttypes.models import ContentType
from vote.models import Vote 

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


class VoteView(LoginRequiredMixin, View):
    '''Like and dislike an object'''
    def post(self, request, *args, **kwargs):
        if is_ajax(request):

            if (object_id:=request.POST.get('object_id')) and \
                (content_type_id:=request.POST.get('content_type_id')) and \
                    (action:=request.POST.get('vote_action')):


                content_type_model = get_object_or_404(ContentType, id=content_type_id)
                object = get_object_or_404(content_type_model.model_class(), id=object_id)
                
                if action == "like":
                    if (vote:=Vote.objects.filter(user=self.request.user, vote="l", \
                                    content_type=content_type_model, object_id=object_id).first()):
                        vote.delete()

                    elif (vote:=Vote.objects.filter(user=self.request.user, vote="d", \
                                    content_type=content_type_model, object_id=object_id).first()):
                        vote.vote = "l"
                        vote.save()

                    else:
                        Vote.objects.create(user=self.request.user, vote="l", 
                                        content_type=content_type_model, object_id=object_id)
                
                if action == "dislike":
                    if (vote:=Vote.objects.filter(user=self.request.user, vote="d", \
                                    content_type=content_type_model, object_id=object_id).first()):
                        vote.delete()
                    
                    elif (vote:=Vote.objects.filter(user=self.request.user, vote="l", \
                                    content_type=content_type_model, object_id=object_id).first()):
                        vote.vote = "d"
                        vote.save()
                        
                    else:
                        Vote.objects.create(user=self.request.user, vote="d", 
                                        content_type=content_type_model, object_id=object_id)

                return JsonResponse({'likes': object.vote.likes(), "dislikes" : object.vote.dislikes()})

            return JsonResponse({'error':'invalid information'})

        return redirect("orders:product-list")
