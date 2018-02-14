from django import forms

#import the actual team model for the create team forms
from teams.models import Team

#import the model for the team invite
from teams.models import TeamInvite

from teams.models import CaptainInvite

#forms to create a team of various sizes

class TeamCreateForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('name','founder')

#invite forms to invite players to a team

class TeamInviteForm(forms.ModelForm):
    class Meta:
        model = TeamInvite
        #maybe????
        fields = ('user','team','inviter')

class CaptainInviteForm(forms.ModelForm):
    class Meta:
        model = CaptainInvite
        #ensure that when the teams are dispalyed they have the proper role to add other captains
        fields = ('user', 'team','inviter')
