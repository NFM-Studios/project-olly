from django import forms
from django.db.models import Q

from teams.models import Team, TeamInvite
from wagers.models import WagerChallenge, WagerRequest


class WagerRequestForm(forms.ModelForm):
    class Meta:
        model = WagerRequest
        fields = ('credits', 'game', 'platform', 'bestof', 'teamformat', 'info', 'team')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.creator = self.user
        # self.user = request.user
        # invites = TeamInvite.objects.filter(hasPerms=True, user=request.user, accepted=True)
        teams = Team.objects.filter(Q(captain__username__contains=self.user) | Q(founder=self.user))
        super(WagerRequestForm, self).__init__(*args, **kwargs)
        self.fields['team'].queryset = teams


class WagerChallengeForm(forms.ModelForm):
    class Meta:
        model = WagerChallenge
        fields = ('team', 'info', 'confirm')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        # invites = TeamInvite.objects.filter(hasPerms=True, user=request.user, accepted=True)
        teams = Team.objects.filter(Q(captain__username__contains=self.user) | Q(founder=self.user))
        super(WagerChallengeForm, self).__init__(*args, **kwargs)
        self.fields['team'].queryset = teams


class WagerRequestDelete(forms.Form):
    confirm = forms.BooleanField()
