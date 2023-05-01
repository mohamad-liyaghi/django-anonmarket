import secrets
from random import randint

def unique_code_generator(cls):
    '''Create unique token for each Chat or Message'''

    code = secrets.token_hex(randint(1, 20))

    # Check if user with this token does not exist
    if cls.objects.filter(code=code).exists():
        unique_code_generator(cls)
    
    return code