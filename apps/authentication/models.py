from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.contenttypes.fields import GenericRelation

from .managers import AccountManager
from vote.models import Vote

class Account(AbstractBaseUser, PermissionsMixin):
    '''Custom user model that allows user to log in with nick_name'''

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
