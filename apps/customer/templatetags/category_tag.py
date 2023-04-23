from django import template
from products.models import Category

register = template.Library()

@register.inclusion_tag('base/sidebar.html')
def category_sidebar():
    '''Return list of categories'''

    return {
        "categories" : Category.objects.select_related("parent") \
                            .filter(parent__isnull=True)[:30]
    }
    

