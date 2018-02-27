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
    class Meta:
        user = forms.CharField(max_length=50, help_text='Required')
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

