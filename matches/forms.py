from django import forms

from matches.models import MatchReport, MatchDispute, Match
from teams.models import Team


class MatchReportCreateFormGet(forms.ModelForm):
    reported_winner = forms.ModelChoiceField(queryset=None)

    class Meta:
        model = MatchReport
        fields = ()

    def __init__(self, request, pk, *args, **kwargs):
        self.username = request.user
        self.reporting_user = request.user
        match = Match.objects.filter(id=pk)
        team1 = Team.objects.filter(id__in=match.values_list('hometeam', flat=True))
        team2 = Team.objects.filter(id__in=match.values_list('awayteam', flat=True))
        super().__init__(*args, **kwargs)
        self.fields['reported_winner'].widget.attrs.update(
            {'name': 'reported_winner', 'class': 'form-control', 'style': 'background-color: black'})
        self.fields['reported_winner'].queryset = team1 | team2


class MatchReportCreateFormPost(forms.ModelForm):
    class Meta:
        model = MatchReport
        fields = ('reported_winner', 'match',)


class DisputeCreateForm(forms.ModelForm):
    # teamproof_1 = forms.URLField()
    # teamproof_2 = forms.URLField()
    # teamproof_3 = forms.URLField()

    class Meta:
        model = MatchDispute
        fields = ['teamproof_1', 'teamproof_2', 'teamproof_3']
