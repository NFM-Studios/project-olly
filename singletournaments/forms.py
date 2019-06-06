from django import forms

from singletournaments.models import SingleEliminationTournament
from teams.models import Team, TeamInvite
from matches.models import PlatformChoice, GameChoice


class SingleEliminationTournamentJoinGet(forms.ModelForm):
    teams = forms.ModelChoiceField(queryset=None)

    # tournaments = forms.ModelChoiceField(queryset=SingleEliminationTournament.objects.all())

    class Meta:
        model = SingleEliminationTournament
        fields = ()

    def __init__(self, request, *args, **kwargs):
        self.username = request.user
        invites = TeamInvite.objects.filter(hasPerms=True, user_id=self.username.id)
        team = Team.objects.filter(id__in=invites.values_list('team', flat=True))
        super().__init__(*args, **kwargs)
        self.fields['teams'].widget.attrs.update({'name': 'teams', 'class': 'form-control'})
        self.fields['teams'].queryset = team


class SingleEliminationTournamentJoinPost(forms.ModelForm):
    teams = forms.ModelChoiceField(queryset=Team.objects.all())

    # tournaments = forms.ModelChoiceField(queryset=SingleEliminationTournament.objects.all())

    class Meta:
        model = SingleEliminationTournament
        fields = ()


class SingleEliminationTournamentSort(forms.Form):
    platform = forms.ChoiceField()
    game = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        platforms = list((obj.id, obj.name) for obj in PlatformChoice.objects.all())
        games = list((obj.id, obj.name) for obj in GameChoice.objects.all())

        platforms.insert(0, ('all', 'All Platforms'))
        games.insert(0, ('all', 'All Games'))

        super(SingleEliminationTournamentSort, self).__init__(*args, **kwargs)

        self.fields['platform'].choices = platforms
        self.fields['game'].choices = games

        self.fields['platform'].widget.attrs.update(
            {'name': 'subject', 'class': 'form-control', 'style': 'background-color: black'})
        self.fields['game'].widget.attrs.update(
            {'name': 'subject', 'class': 'form-control', 'style': 'background-color: black'})


class SingleTournamentLeaveForm(forms.Form):
    confirm = forms.BooleanField(required=False)

    class Meta:
        fields = 'Confirm'
