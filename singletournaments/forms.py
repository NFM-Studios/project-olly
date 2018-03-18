from django import forms
from singletournaments.models import SingleEliminationTournament


class SingleEliminationTournamentJoin(forms.ModelForm):
    class Meta:
        model = SingleEliminationTournament
        fields = ('teams', )
