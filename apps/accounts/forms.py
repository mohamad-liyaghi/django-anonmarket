from django import forms
from accounts.models import Account

class RegisterForm(forms.ModelForm):
    '''A form for creating user'''

    class Meta:
        model = Account
        fields = ["username", "password"]

        widgets = {
        'username': forms.TextInput(attrs={'placeholder': 'Select a unique username.'}),
        'password': forms.PasswordInput(attrs={'placeholder': 'Enter your password.'})
    }


    def save(self, commit):
        '''Call create_user when creating a user with forms'''

        return Account.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['password']
        )
