from django import forms
from singletournaments.models import SingleEliminationTournament
from teams.models import Team


class SingleEliminationTournamentJoin(forms.ModelForm):
    teams = forms.ModelChoiceField(queryset=Team.objects.all())
    tournaments = forms.ModelChoiceField(queryset=SingleEliminationTournament.objects.all())
    class Meta:
        model = SingleEliminationTournament
        fields = ()
