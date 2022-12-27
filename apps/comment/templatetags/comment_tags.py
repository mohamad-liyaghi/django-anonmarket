from django import template
from django.db.models import Q

register = template.Library()

@register.filter
def get_object_comments(obj):
    #TODO add rate to orders
    if obj.comment:
        return obj.comment.all().order_by("-pinned", "-date")

    return None

