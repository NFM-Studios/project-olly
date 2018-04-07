from django import forms
from matches.models import MatchReport, MatchDispute
from teams.models import Team


class MatchReportCreateForm(forms.ModelForm):
    class Meta:
        model = MatchReport
        fields = ( 'reported_winner', 'match', )

    def __init__(self, request, *args, **kwargs):
        self.username = request.user
        self.reporting_user = request.user
        self.reporting_team = forms.ModelChoiceField(queryset=Team.objects.filter(captain=['captain', 'founder'], user_id=self.username.id))
        super(MatchReportCreateForm, self).__init__(*args, **kwargs)


class DisputeCreateForm(forms.ModelForm):
    teamproof_1 = forms.URLField()
    teamproof_2 = forms.URLField()
    teamproof_3 = forms.URLField()
    class Meta:
        model = MatchDispute
        fields = ('teamproof', 'match')

    def __init__(self, request, *args, **kwargs):
        self.teamreporter = request.user
        super(DisputeCreateForm, self).__init__(*args, **kwargs)
