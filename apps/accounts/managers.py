from django.contrib.auth.models import BaseUserManager
import random

class AccountManager(BaseUserManager):

    def create_user(self, username, password, **kwargs):
        '''Create a new user'''
        token = random.randint(0, 9999999999999999999)
        user = self.model(username= username, token=token, **kwargs)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, password):
        '''Create a new superuser'''
        return self.create_user(username, password, is_staff=True, is_superuser=True, is_active=True)
