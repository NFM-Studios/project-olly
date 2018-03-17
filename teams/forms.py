from django import forms

# import the actual team model for the create team forms
from teams.models import Team

# import the model for the team invite
from teams.models import TeamInvite

# forms to create a team of various sizes


class TeamCreateForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('name',)

# invite forms to invite players to a team


class TeamInviteForm(forms.ModelForm):
    user = forms.CharField(required=True, max_length=50)

    class Meta:
        # team = forms.?
        captain = forms.BooleanField(required=False)
        model = TeamInvite
        # maybe????
        fields = ('user', 'team', 'captain',)
        # widgets = {
        #    'user':CharField(),
        # }


class EditTeamProfileForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = (
            'about_us',
            'website',
            'twitter',
            'twitch',
        )


class ViewInviteForm(forms.ModelForm):
    accepted = forms.BooleanField(required=False)
    denied = forms.BooleanField(required=False)

    class Meta:
        model = TeamInvite
        fields = {
            'accepted',
            'denied'
        }


class LeaderboardSortForm(forms.Form):      # it works but is messy af. should be replaced with something like http://img.mulveyben.me/img/chrome_2018-03-11_22-04-28.png
    sort_xp_asc = forms.BooleanField(required=False)
    sort_xp_desc = forms.BooleanField(required=False)
    sort_trophies_asc = forms.BooleanField(required=False)
    sort_trophies_desc = forms.BooleanField(required=False)


