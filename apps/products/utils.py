from django.utils.text import slugify
import secrets
from random import randint

def unique_slug_generator(title:str, cls):
    '''Create unique token for each user'''

    slugified_title = slugify(title)

    prefix = secrets.token_hex(randint(1, 5))
    slug = slugified_title + prefix

    # Check if user with this token does not exist
    if cls.objects.filter(slug=slug).exists():
        unique_slug_generator(cls)
    
    return slug