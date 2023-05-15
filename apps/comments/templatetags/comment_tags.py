from django import template
from django.db.models import Q

register = template.Library()

@register.filter
def get_object_top_comments(obj):
    if obj.comments:
        return obj.comments.select_related('user').filter(parent=None).order_by("-is_pinned", "-votes", "-date")[:5]

    return None

