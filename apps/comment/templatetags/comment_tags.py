from django import template
from django.db.models import Q

register = template.Library()

@register.filter
def get_object_comments(obj):
    if obj.comment:
        return obj.comment.filter(parent=None).order_by("-pinned", "-vote", "-date")

    return None

