from django import forms
from django.contrib.auth.models import User

from .models import UserProfile


class CreateUserForm(forms.ModelForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)
    tos = forms.BooleanField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'name': 'username', 'class': 'form-control', 'style': 'width:30%'})
        self.fields['email'].widget.attrs.update({'name': 'email', 'class': 'form-control', 'style': 'width:30%'})
        self.fields['password'].widget.attrs.update({'name': 'password', 'class': 'form-control', 'style': 'width:30%'})
        self.fields['password_confirm'].widget.attrs.update({'name': 'password_confirm', 'class': 'form-control',
                                                             'style': 'width:30%'})


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = (
            'profile_picture',
            'about_me',
            'xbl',
            'psn',
            'steam',
            'epic',
            'lol',
            'battlenet',
            'twitter_profile',
            'twitch_channel',
            'favorite_game',
            'favorite_console',
            'country',
            'email_enabled'
        )

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields['profile_picture'].widget.attrs.update(
            {'name': 'profile_picture', 'class': 'form-control', 'style': ''})
        self.fields['about_me'].widget.attrs.update({'name': 'about_me', 'class': 'form-control', 'style': ''})
        self.fields['xbl'].widget.attrs.update({'name': 'xbl', 'class': 'form-control', 'style': ''})
        self.fields['psn'].widget.attrs.update({'name': 'psn', 'class': 'form-control',
                                                'style': ''})
        self.fields['steam'].widget.attrs.update({'name': 'steam', 'class': 'form-control', 'style':
            ''})
        self.fields['epic'].widget.attrs.update({'name': 'epic', 'class': 'form-control', 'style':
            ''})
        self.fields['battlenet'].widget.attrs.update({'name': 'battlenet', 'class': 'form-control', 'style':
            ''})
        self.fields['twitter_profile'].widget.attrs.update({'name': 'twitter_profile', 'class': 'form-control', 'style':
            ''})
        self.fields['twitch_channel'].widget.attrs.update({'name': 'twitch_channel', 'class': 'form-control', 'style':
            ''})
        self.fields['favorite_game'].widget.attrs.update({'name': 'favorite_game', 'class': 'form-control', 'style':
            ''})
        self.fields['favorite_console'].widget.attrs.update(
            {'name': 'favorite_console', 'class': 'form-control', 'style':
                ''})
        self.fields['country'].widget.attrs.update({'name': 'country', 'class': 'form-control',
                                                    'style': 'background-color: black;'})
        self.fields['email_enabled'].widget.attrs.update({'name': 'email_enabled', 'class': 'form-control',
                                                          'style': 'background-color: black;'})


class SortForm(forms.Form):  # it works but is messy af. should be replaced with something like
    # http://img.mulveyben.me/img/chrome_2018-03-11_22-04-28.png
    sort_xp_asc = forms.BooleanField(required=False)
    sort_xp_desc = forms.BooleanField(required=False)
    sort_trophies_asc = forms.BooleanField(required=False)
    sort_trophies_desc = forms.BooleanField(required=False)
    sort_rank_asc = forms.BooleanField(required=False)
    sort_rank_desc = forms.BooleanField(required=False)
