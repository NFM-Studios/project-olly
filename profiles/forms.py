from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django import forms
from .models import UserProfile

class CreateUserForm(forms.ModelForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = (
            'profile_picture',
            'about_me',
            'xbl',
            'psn',
            'twitter_profile',
            'twitch_channel',
            'favorite_game',
            'favorite_console',
            #profile picture
        )
