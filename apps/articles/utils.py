from django.utils.text import slugify
import secrets
from random import randint

def unique_slug_generator(title:str, cls):
    '''Create unique token for each article'''

    slugified_title = slugify(title)

    prefix = secrets.token_hex(randint(1, 5))
    slug = slugified_title + prefix

    # Check if user with this token does not exist
    if cls.objects.filter(slug=slug).exists():
        unique_slug_generator(cls)
    
    return slug

def unique_token_generator(cls):
    '''Create unique token for each article purchase'''
    token = secrets.token_hex(randint(1, 20))
    if cls.objects.filter(token=token).exists():
        unique_token_generator(cls)
    
    return token