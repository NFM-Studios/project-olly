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
        self.fields['teams'].widget.attrs.update({'name': 'teams', 'class': 'form-control'})
        self.fields['teams'].queryset = team


class SingleEliminationTournamentJoinPost(forms.ModelForm):
    teams = forms.ModelChoiceField(queryset=Team.objects.all())
    # tournaments = forms.ModelChoiceField(queryset=SingleEliminationTournament.objects.all())

    class Meta:
        model = SingleEliminationTournament
        fields = ()


class SingleEliminationTournamentSort(forms.Form):
    platform = forms.ChoiceField()
    game = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        platforms = (
            (0, 'Playstation 4'),
            (1, 'Xbox One'),
            (2, 'PC'),
            (3, 'Mobile'),
            (4, 'Nintendo Switch'),
            (5, 'Playstation 3'),
            (6, 'Xbox 360'),
            (7, 'Any')
        )

        games = (
            (0, 'No Game Set'),
            (1, 'Call of Duty Black Ops 3'),
            (2, 'Call of Duty WWII'),
            (3, 'Fortnite'),
            (4, 'Destiny 2'),
            (5, 'Counter-Strike: Global Offensive'),
            (6, 'Player Unknowns Battlegrounds'),
            (7, 'Rainbow Six Siege'),
            (8, 'Overwatch'),
            (9, 'League of Legends'),
            (10, 'Hearthstone'),
            (11, 'World of Warcraft'),
            (12, 'Smite'),
            (13, 'Rocket League'),
            (14, 'Battlefield 1'),
            (15, 'Black Ops 4'),
            (16, 'Any')
        )
        super(SingleEliminationTournamentSort, self).__init__(*args, **kwargs)
        self.fields['platform'].choices = platforms
        self.fields['game'].choices = games
        self.fields['platform'].widget.attrs.update({'name': 'subject', 'class': 'form-control', 'style': 'background-color: black'})
        self.fields['game'].widget.attrs.update({'name': 'subject', 'class': 'form-control', 'style': 'background-color: black'})


class SingleTournamentLeaveForm(forms.Form):
    confirm = forms.BooleanField(required=False)
    class Meta:
        fields = 'Confirm'
