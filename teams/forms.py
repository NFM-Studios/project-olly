from django import forms

#import the actual team model for the create team forms
from teams.models import Team

#import the model for the team invite
from teams.models import TeamInvite

fron teams.models import CaptainInvite

#forms to create a team of various sizes

class TeamCreateForm(forms.ModelForm):
    class Meta:
        model = soloTeam
        fields = ('name')




#invite forms to invite players to a team

class TeamInviteForm(forms.ModelForm):
    class Meta:
        model = duoTeamInvite
        #maybe????
        fields = ('user')
