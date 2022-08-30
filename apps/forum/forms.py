from django import forms
from forum.models import Forum


class ForumForm(forms.ModelForm):
    '''A form for creating Forums'''

    class Meta:
        model = Forum
        fields = fields = ("title", "body", "price")