from django.contrib.auth.models import User
from django import forms
from .models import UserProfile


class CreateUserForm(forms.ModelForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)
    tos = forms.BooleanField(required=True)

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
            'country'
        )


class SortForm(forms.Form):      # it works but is messy af. should be replaced with something like http://img.mulveyben.me/img/chrome_2018-03-11_22-04-28.png
    sort_xp_asc = forms.BooleanField(required=False)
    sort_xp_desc = forms.BooleanField(required=False)
    sort_trophies_asc = forms.BooleanField(required=False)
    sort_trophies_desc = forms.BooleanField(required=False)
