from django import forms
# import the actual team model for the create team forms
from teams.models import Team
# import the model for the team invite
from teams.models import TeamInvite
from profiles.models import UserProfile


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
        fields = ('user', 'team', 'captain')
        widgets = {
            'user': forms.CharField(),
        }

    def __init__(self, request, *args, **kwargs):
        super(TeamInviteFormGet, self).__init__(*args, **kwargs)
        self.fields['captain'].widget.attrs.update(
            {'name': 'captain', 'class': 'form-control', 'style': 'width:30%;display: block'})

        self.username = request.user
        profile = UserProfile.objects.get(user=request.user)
        tlist = profile.captain_teams.all() | profile.founder_teams.all()
        teams = tlist
        self.fields['team'].queryset = teams
        # super().__init__(*args, **kwargs)


class TeamInviteFormPost(forms.ModelForm):
    user = forms.CharField(required=True, max_length=50)

    class Meta:
        captain = forms.BooleanField(required=False)
        model = TeamInvite
        fields = ('user', 'team', 'captain',)
        widgets = {
            'user': forms.CharField(),
        }


class EditTeamProfileForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = (
            'about_us',
            'tag',
            'website',
            'twitter',
            'twitch',
            'country',
            'image'
        )

    def __init__(self, *args, **kwargs):
        super(EditTeamProfileForm, self).__init__(*args, **kwargs)
        self.fields['about_us'].widget.attrs.update({'name': 'about_us', 'class': 'form-control', 'style': 'width:30%'})
        self.fields['tag'].widget.attrs.update({'name': 'about_us', 'class': 'form-control', 'style': 'width:30%'})
        self.fields['website'].widget.attrs.update({'name': 'website', 'class': 'form-control', 'style': 'width:30%'})
        self.fields['twitter'].widget.attrs.update({'name': 'twitter', 'class': 'form-control', 'style': 'width:30%'})
        self.fields['twitch'].widget.attrs.update({'name': 'twitch', 'class': 'form-control', 'style': 'width:30%'})
        self.fields['country'].widget.attrs.update({'name': 'country', 'class': 'form-control', 'style': 'width:30%'})


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

    def __init__(self, request, pk, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['confirmed'].widget.attrs.update(
            {'name': 'confirmed', 'class': 'form-control', 'style': 'display: block'})


class RemoveUserForm(forms.Form):
    remove = forms.ModelChoiceField(queryset=None)

    def __init__(self, request, pk, *args, **kwargs):
        team = Team.objects.get(id=pk)
        players = team.players.all() | team.captain.all()
        super().__init__(*args, **kwargs)
        self.fields['remove'].queryset = players
        self.fields['remove'].widget.attrs.update(
            {'name': 'remove', 'class': 'form-control', 'style': 'background-color: black'})


class RemovePlayerFormPost(forms.Form):
    remove = forms.ModelChoiceField(queryset=None)


class DissolveTeamForm(forms.Form):
    confirmed = forms.BooleanField(required=False)
