from django.views.generic import ListView
from django.contrib.contenttypes.models import ContentType
from forums.models import ForumAnswer
from forums.mixins import ForumObject


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