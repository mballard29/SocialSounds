from django import forms
from .models import Item


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)


class PostForm(forms.Form): 
    album_url = forms.CharField(max_length=500, required=True)
    caption = forms.CharField(widget=forms.Textarea(attrs={'class': 'input'}), required=True)
