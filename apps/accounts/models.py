from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.contenttypes.fields import GenericRelation

from .managers import AccountManager
from accounts.utils import unique_token_generator
from vote.models import Vote


class Account(AbstractBaseUser, PermissionsMixin):
    '''Main account model of project'''

    username = models.CharField(max_length=120, unique=True)
    balance = models.IntegerField(default=0)
    token = models.CharField(max_length=20, unique=True)

    date_joined = models.DateField(auto_now_add=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    vote = GenericRelation(Vote, related_query_name="account_vote")
    objects = AccountManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):

        if not self.pk:
            # lower the username
            self.username = self.username.lower()
            # set a unique token for user
            self.token = unique_token_generator(self.__class__)
            # set user as active user
            self.is_active = True
            
            return super().save(*args, **kwargs)

        return super().save(*args, **kwargs)