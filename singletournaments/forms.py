from django import forms
from singletournaments.models import SingleEliminationTournament
from teams.models import Team


class SingleEliminationTournamentJoin(forms.ModelForm):
    teams = forms.ModelChoiceField(queryset=Team.objects.all())
    # tournaments = forms.ModelChoiceField(queryset=SingleEliminationTournament.objects.all())

    class Meta:
        model = SingleEliminationTournament
        fields = ()

    #def __init__(self, request, *args, **kwargs):
    #    self.username = request.user
    #    self.team = forms.ModelChoiceField(
    #        queryset=TeamInvite.objects.filter(captain=['captain', 'founder'], user_id=self.username.id))
    #    super(SingleEliminationTournamentJoin, self).__init__(*args, **kwargs)
