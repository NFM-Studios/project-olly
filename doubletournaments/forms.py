from django import forms

from teams.models import Team


class DoubleEliminationTournamentJoinPost(forms.Form):
    teams = forms.ModelChoiceField(queryset=Team.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['teams'].widget.attrs.update({'name': 'teams', 'class': 'form-control'})


class DoubleEliminationTournamentLeaveForm(forms.Form):
    confirm = forms.BooleanField(required=False)

    class Meta:
        fields = 'Confirm'