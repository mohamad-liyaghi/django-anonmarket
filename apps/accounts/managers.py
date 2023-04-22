from django.contrib.auth.models import BaseUserManager

class AccountManager(BaseUserManager):
    '''This manager allows Account model to use create_user() and create_superuser() methods'''

    def create_user(self, username, password, **kwargs):
        user = self.model(username=username, **kwargs)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, password):
        return self.create_user(
            username,
            password,
            is_staff=True,
            is_superuser=True,
            is_active=True
        )
