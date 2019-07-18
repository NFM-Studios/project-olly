from django import forms
from django.db.models import Q

from teams.models import Team
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
        super(WagerRequestForm, self).__init__(*args, **kwargs)
        self.fields['credits'].widget.attrs.update({'name': 'credits', 'class': 'form-control'})
        self.fields['game'].widget.attrs.update(
            {'name': 'game', 'class': 'form-control', 'style': 'background-color:#141a20'})
        self.fields['platform'].widget.attrs.update({'name': 'platform', 'class': 'form-control', 'style': 'background-color:#141a20'})
        self.fields['bestof'].widget.attrs.update(
            {'name': 'bestof', 'class': 'form-control', 'style': 'background-color:#141a20'})
        self.fields['teamformat'].widget.attrs.update(
            {'name': 'teamformat', 'class': 'form-control', 'style': 'background-color:#141a20'})
        self.fields['info'].widget.attrs.update(
            {'name': 'info', 'class': 'form-control', 'style': 'background-color:#141a20'})
        self.fields['team'].widget.attrs.update(
            {'name': 'team', 'class': 'form-control', 'style': 'background-color:#141a20'})


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
