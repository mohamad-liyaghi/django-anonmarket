from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

from django.contrib.contenttypes.models import ContentType
from votes.models import Vote 

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


class VoteView(LoginRequiredMixin, View):
    '''Upvote and downvote an object'''

    def post(self, request, *args, **kwargs):
        # Only ajax requests are allowed
        if not is_ajax(request):
            return redirect("orders:product-list")

        object_id = request.POST.get('object_id')
        content_type_id = request.POST.get('content_type_id')
        choice = request.POST.get('choice')

        if not all([object_id, content_type_id, choice]):
            return JsonResponse({'error': 'invalid information'})

        # Get the content type and object for the given IDs
        content_type = get_object_or_404(ContentType, id=content_type_id)
        obj = get_object_or_404(content_type.model_class(), id=object_id)

        # Create a new vote object
        if choice == "upvote":
            vote_choice = "u"

        elif choice == "downvote":
            vote_choice = "d"

        else:
            return JsonResponse({'error': 'invalid choice'})

        Vote.objects.create(
            user=request.user,
            choice=vote_choice,
            content_type=content_type,
            object_id=object_id
        )

        # Return the upvote and downvote counts for the object
        return JsonResponse({
            'upvotes': obj.votes.upvotes_count(),
            'downvotes': obj.votes.downvotes_count()
        })
