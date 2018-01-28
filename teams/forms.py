from django import forms

#import the actual team model for the create team forms
from teams.models import soloTeam, duoTeam, trioTeam, quadTeam, fiveTeam, sixTeam

#import the model for the team invite
from teams.models import duoTeamInvite, trioTeamInvite, quadTeamInvite, fiveTeamInvite, sixTeamInvite

#forms to create a team of various sizes

class soloTeamCreateForm(forms.ModelForm):
    class Meta:
        model = soloTeam
        fields = ('name')

class duoTeamCreateForm(forms.ModelForm):
    class Meta:
        model = duoTeam
        fields = ('name')

class trioTeamCreateForm(forms.ModelForm):
    class Meta:
        model = trioTeam
        fields = ('name')

class quadTeamCreateForm(forms.ModelForm):
    class Meta:
        model = quadTeam
        fields = ('name')

class fiveTeamCreateForm(forms.ModelForm):
    class Meta:
        model = fiveTeam
        fields = ('name')

class sixTeamCreateForm(forms.ModelForm):
    class Meta:
        model = sixTeam
        fields = ('name')



#invite forms to invite players to a team

class duoTeamInviteForm(forms.ModelForm):
    class Meta:
        model = duoTeamInvite
        #maybe????
        fields = ('user')

class trioTeamInviteForm(forms.ModelForm):
    class Meta:
        model = trioTeamInvite
        #pls work
        fields = ('user')

class quadTeamInviteForm(forms.ModelForm):
    class Meta:
        model = quadTeamInvite
        #pls
        fields = ('user')

class fiveTeamInviteForm(forms.ModelForm):
    class Meta:
        model = fiveTeamInvite
        #pls
        fields = ('user')

class sixTeamInviteForm(forms.ModelForm):
    class Meta:
        model = sixTeamInvite
        #pls
        fields = ('user')
