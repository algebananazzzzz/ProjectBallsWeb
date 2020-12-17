from django import forms
from .models import User, BoardModel, SnippetModel
from django.contrib.auth.forms import UserCreationForm


class signupForm(UserCreationForm):
    class Meta:
        model = User

        fields = ('username',)


class configureUserForm(forms.ModelForm):
    class Meta:
        model = User

        fields = ('username', 'start_recording_key',
                  'end_recording_key', 'cancel_recording_key')


class BoardModelForm(forms.ModelForm):

    Name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'validate require-count', 'data-length': 50}))

    Description = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'class': 'validate materialize-textarea require-count', 'data-length': 500}))

    class Meta:
        model = BoardModel
        fields = ('Name', 'primaryTags', 'Description',
                  'videoFile', 'thumbnail')
    
    def __init__(self, *args, **kwargs):
        super(BoardModelForm, self).__init__(*args, **kwargs)
        self.fields['primaryTags'].required = False

