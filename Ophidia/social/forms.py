from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    body = forms.CharField(
        label = '',
        widget = forms.Textarea(attrs = {
            'rows': 3,
            'placeholder': "Enter your text post here",
        })
    )
    class Meta:
        model = Post
        fields = ['body']

class CommentForm(forms.ModelForm):
    comment = forms.CharField(
        label = '',
        widget = forms.Textarea(attrs = {
            'rows': 3,
            'placeholder': "Type your comment here",
        })
    )
    class Meta:
        model = Comment
        fields = ['comment']

class ThreadForm(forms.Form):
    username = forms.CharField(label = '', max_length = 100)

class MessageForm(forms.Form):
    message = forms.CharField(label = '', max_length = 100)