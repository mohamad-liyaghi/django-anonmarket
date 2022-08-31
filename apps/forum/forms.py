from django import forms
from forum.models import Forum, ForumComment


class ForumForm(forms.ModelForm):
    '''A form for creating Forums'''

    class Meta:
        model = Forum
        fields = fields = ("title", "body", "price")


class CommentForm(forms.ModelForm):
    class Meta:
        model = ForumComment
        fields = ("forum", "body", "user")