import secrets
from random import randint

def unique_order_token_generator(cls):
    '''Create unique token for each user'''
    token = secrets.token_hex()[:randint(1, 19)]

    # Check if user with this token does not exist
    if cls.objects.filter(token=token).exists():
        unique_order_token_generator(cls)
    
    return token