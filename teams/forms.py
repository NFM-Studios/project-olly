from django import forms

from django.forms import ModelForm

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


class TeamInviteFormGet(forms.ModelForm):
    user = forms.CharField(required=True, max_length=50)
    team = forms.ModelChoiceField(queryset=None)

    class Meta:
        captain = forms.BooleanField(required=False)
        model = TeamInvite
        # maybe????
        fields = ('user', 'team', 'captain',)
        widgets = {
            'user': forms.CharField(),
         }

    def __init__(self, request, *args, **kwargs):
        self.username = request.user
        invites = TeamInvite.objects.filter(hasPerms=True, user=request.user, accepted=True)
        teams = Team.objects.filter(id__in=invites.values_list('team'))
        super().__init__(*args, **kwargs)
        self.fields['team'].queryset = teams



class TeamInviteFormPost(forms.ModelForm):
    user = forms.CharField(required=True, max_length=50)

    class Meta:
        captain = forms.BooleanField(required=False)
        model = TeamInvite
        # maybe????
        fields = ('user', 'team', 'captain',)
        widgets = {
            'user': forms.CharField(),
         }


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


class LeaveTeamForm(forms.Form):
    confirmed = forms.BooleanField(required=False)
