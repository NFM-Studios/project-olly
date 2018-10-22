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

    def __init__(self, *args, **kwargs):
        super(TeamCreateForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'name': 'name', 'class': 'form-control', 'style': 'width:30%'})


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
        super(TeamInviteFormGet, self).__init__(*args, **kwargs)
        self.fields['user'].widget.attrs.update({'name': 'user', 'class': 'form-control', 'style': 'width:30%'})
        self.fields['team'].widget.attrs.update({'name': 'team', 'class': 'form-control', 'style': 'width:30%'})
        self.fields['captain'].widget.attrs.update({'name': 'captain', 'class': 'form-control', 'style': 'width:30%'})

        self.username = request.user
        invites = TeamInvite.objects.filter(hasPerms=True, user=request.user, accepted=True)
        teams = Team.objects.filter(id__in=invites.values_list('team'))
        # super().__init__(*args, **kwargs)
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

    def __init__(self, *args, **kwargs):
        super(EditTeamProfileForm, self).__init__(*args, **kwargs)
        self.fields['about_us'].widget.attrs.update({'name': 'about_us', 'class': 'form-control', 'style': 'width:30%'})
        self.fields['website'].widget.attrs.update({'name': 'website', 'class': 'form-control', 'style': 'width:30%'})
        self.fields['twitter'].widget.attrs.update({'name': 'twitter', 'class': 'form-control', 'style': 'width:30%'})
        self.fields['twitch'].widget.attrs.update({'name': 'twitch', 'class': 'form-control', 'style': 'width:30%'})


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


class RemoveUserForm(forms.Form):
    remove = forms.ModelChoiceField(queryset=None)

    def __init__(self, request, pk, *args, **kwargs):
        team = Team.objects.get(id=pk)
        players = TeamInvite.objects.filter(team=team, accepted=True)
        super().__init__(*args, **kwargs)
        self.fields['remove'].queryset = players
        self.fields['remove'].widget.attrs.update({'name': 'remove', 'class': 'form-control', 'style': 'background-color: black'})



class RemovePlayerFormPost(forms.Form):
    remove = forms.ModelChoiceField(queryset=None)


class DissolveTeamForm(forms.Form):
    confirmed = forms.BooleanField(required=False)