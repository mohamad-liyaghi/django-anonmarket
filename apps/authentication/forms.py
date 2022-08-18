from django import forms
from authentication.models import Account
import random

class RegisterForm(forms.ModelForm):
    '''A form for creating user'''

    class Meta:
        model = Account
        fields = ("username", "password")

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = "Select a unique username, not using your real name is recommended"
        self.fields['password'].widget.attrs['placeholder'] = "Select a strong password"

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = True
        user.token = random.randint(0, 9999999999999999999)
        user.save()
        return user
