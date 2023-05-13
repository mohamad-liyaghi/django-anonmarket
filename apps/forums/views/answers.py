from django.views.generic import ListView, View
from django.shortcuts import redirect
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from forums.models import ForumAnswer
from forums.mixins import ForumObject

def is_ajax(request):
    '''Check if a request is ajax or not'''
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


class ForumAnswerCreateView(LoginRequiredMixin, ForumObject, View):
    def get(self, request, *args, **kwargs):
        return redirect("forums:forum-list")

    def post(self, request, *args, **kwargs):
        if is_ajax(request):
            object_id = request.POST.get('object_id')
            object_slug = request.POST.get('object_slug')
            content = request.POST.get('content')

            if object_id and object_slug and content:
                if self.forum.closed:
                    return JsonResponse({'closed':'forum is closed'})
                
                answer = ForumAnswer.objects.create(forum=self.forum, user=self.request.user, answer=content)
                # Create the comment here
                return JsonResponse({'created': 'answer created', 'date' : answer.date, 'answer' : answer.answer})
            
            return JsonResponse({'error':'invalid information'})
        
        return redirect("forums:forum-list")

class ForumAnswerListView(ForumObject, ListView):
    template_name = 'answers/forum-answer-list.html'
    context_object_name = 'answers'

    def get_queryset(self):
        return ForumAnswer.objects.filter(forum=self.forum).order_by('-is_correct_answer', '-date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        content_type = ContentType.objects.get_for_model(ForumAnswer)
        context['model_content_type_id'] = content_type.id
        return context