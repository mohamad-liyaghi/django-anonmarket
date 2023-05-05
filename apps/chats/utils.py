import secrets
from random import randint

def unique_code_generator(cls):
    '''Create unique token for each Chat or Message'''

    code = secrets.token_hex(randint(1, 20))

    # Check if user with this token does not exist
    if cls.objects.filter(code=code).exists():
        unique_code_generator(cls)
    
    return code

def set_chat_participant(participant_model, chat, participants:list):
    for participant in participants:
        participant_model.objects.create(user=participant, chat=chat)