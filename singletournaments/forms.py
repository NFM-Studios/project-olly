from django import forms
from singletournaments.models import SingleEliminationTournament


class SingleEliminationTournamentJoin(forms.ModelForm):
    tournaments = forms.ModelChoiceField(queryset=SingleEliminationTournament.objects.all())
    class Meta:
        model = SingleEliminationTournament
        fields = ('teams', )
