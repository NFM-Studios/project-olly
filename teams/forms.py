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


class TeamInviteForm(forms.ModelForm):
    user = forms.CharField(required=True, max_length=50)

    class Meta:
        captain = forms.BooleanField(required=False)
        model = TeamInvite
        # maybe????
        fields = ('user', 'team', 'captain',)
        widgets = {
            'user':forms.CharField(),
         }

    def __init__(self, request, *args, **kwargs):
        self.username = request.user
        self.team = forms.ModelChoiceField(queryset=TeamInvite.objects.filter(captain=['captain', 'founder'], user_id=self.username.id))
        super(TeamInviteForm, self).__init__(*args, **kwargs)


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


