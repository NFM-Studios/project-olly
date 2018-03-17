from django import forms
from matches.models import MatchReport


class MatchReportCreateForm(forms.ModelForm):
    class Meta:
        model = MatchReport
        fields = ( 'reported_winner', 'match', )
