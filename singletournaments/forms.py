from django import forms
from singletournaments.models import SingleEliminationTournament
from teams.models import Team, TeamInvite


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
        self.fields['teams'].queryset = team


class SingleEliminationTournamentJoinPost(forms.ModelForm):
    teams = forms.ModelChoiceField(queryset=Team.objects.all())
    # tournaments = forms.ModelChoiceField(queryset=SingleEliminationTournament.objects.all())

    class Meta:
        model = SingleEliminationTournament
        fields = ()
