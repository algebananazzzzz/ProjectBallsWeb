from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm


class signupForm(UserCreationForm):
    class Meta:
        model = User

        fields = ('username',)