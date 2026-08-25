from django import forms

from .models import League


class LeagueJoinForm(forms.Form):
    # team the user wants to enter into the league; restricted to teams the
    # acting user founds or captains
    team = forms.ModelChoiceField(queryset=None)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['team'].queryset = user.user.founder_teams.all() | user.user.captain_teams.all()


class LeagueLeaveForm(forms.Form):
    # team the user wants to remove from the league
    team = forms.ModelChoiceField(queryset=None)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['team'].queryset = user.user.founder_teams.all() | user.user.captain_teams.all()