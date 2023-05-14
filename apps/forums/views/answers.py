from django.forms.models import BaseModelForm
from django.views.generic import ListView, View, UpdateView, DeleteView
from django.shortcuts import redirect, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
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
        return ForumAnswer.objects.select_related('user').filter(forum=self.forum).order_by('-is_correct_answer', '-date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        content_type = ContentType.objects.get_for_model(ForumAnswer)
        context['model_content_type_id'] = content_type.id
        context['forum'] = self.forum
        return context


class ForumAnswerUpdateView(LoginRequiredMixin, ForumObject, UpdateView):
    
    template_name = 'answers/update-forum-answer.html'
    fields = ['answer']

    def get_object(self):
        return get_object_or_404(
            ForumAnswer, forum=self.forum, user=self.request.user,
            id=self.kwargs['answer_id'],
            token=self.kwargs['answer_token'],
        )
    
    def form_valid(self, form):
        messages.success(self.request, 'Answer Updated', 'success')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("forums:forum-answer-list", kwargs={"id" : self.forum.id, "slug" : self.forum.slug})


class ForumAnswerDeleteView(LoginRequiredMixin, ForumObject, DeleteView):
    
    template_name = 'answers/delete-forum-answer.html'

    def get_object(self):
        return get_object_or_404(
            ForumAnswer, forum=self.forum, user=self.request.user,
            id=self.kwargs['answer_id'],
            token=self.kwargs['answer_token'],
        )
    
    def post(self, request, *args, **kwargs):
        messages.success(request, 'Answer Deleted!', 'danger')
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("forums:forum-answer-list", kwargs={"id" : self.forum.id, "slug" : self.forum.slug})
