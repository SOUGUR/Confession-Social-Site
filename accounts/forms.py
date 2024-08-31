# accounts/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Post

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['confession']

    def save(self, commit=True, user=None):
        post = super().save(commit=False)
        post.user = user
        if commit:
            post.save()
        return post