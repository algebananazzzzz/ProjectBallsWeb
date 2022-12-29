from django import forms
from .models import User, BoardModel
from django.contrib.auth.forms import UserCreationForm


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User

        fields = ('username', 'password1', 'password2')


class configureUserForm(forms.ModelForm):
    class Meta:
        model = User

        fields = ('start_recording_key', 'end_recording_key',
                  'cancel_recording_key')


class BoardModelForm(forms.ModelForm):

    Name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'data-length': 100}))

    Description = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'class': 'form-control', 'data-length': 500}))

    videoFile = forms.FileField(required=False, widget=forms.FileInput(
        attrs={'class': 'form-control', 'accept': 'video/*'}))

    thumbnail = forms.FileField(required=False, widget=forms.FileInput(
        attrs={'class': 'form-control', 'accept': 'image/*'}))

    class Meta:
        model = BoardModel
        fields = ('Name', 'primaryTags', 'Description',
                  'videoFile', 'thumbnail')

    def __init__(self, *args, **kwargs):
        super(BoardModelForm, self).__init__(*args, **kwargs)
        self.fields['primaryTags'].required = False
