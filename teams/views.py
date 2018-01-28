from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView


#team create forms
from teams.forms import soloTeamCreateForm, duoTeamCreateForm, trioTeamCreateForm, quadTeamCreateForm, fiveTeamCreateForm, sixTeamCreateForm

#team create invite forms
from teams.forms import duoTeamInviteForm, trioTeamInviteForm, quadTeamInviteForm, fiveTeamInviteForm, sixTeamInviteForm

#import the team models
from teams.models import soloTeam, duoTeam, trioTeam, quadTeam, fiveTeam, sixTeam

#import the invite models
from teams.models import duoTeamInvite, trioTeamInvite, quadTeamInvite, sixTeamInvite

class MyInvitesListView(ListView):
# show all the invites, and an accept or deny button.
# check if the invite is expired.


class MyTeamsListView(ListView):
# list all the teams they are apart of
# maybe list the role they have?

#divide it into sections based on solo, duo, trio, quad, five, six?

class MyTeamDetailView(DetailView):
#show team info, allow them to invite users.

class TeamInviteCreateView(CreateView):
#allow the person to create an invite for there team

class SoloTeamCreateView(CreateView):
    form_class=soloTeamCreateForm
    template_name='teams/solo_create.html'

class DuoTeamCreateView(CreateView):
    form_class=duoTeamCreateForm
    template_name='teams/duo_create.html'

class TrioTeamCreateView(CreateView):
    form_class=trioTeamCreateForm
    template_name='teams/trio_create.html'

class QuadTeamCreateView(CreateView):
    form_class=quadTeamCreateForm
    template_name='teams/quad_create.html'

class FiveTeamCreateView(CreateView):
    form_class=fiveTeamCreateForm
    template_name='teams/five_create.html'

class SixTeamCreateView(CreateView):
    form_class=sixTeamCreateForm
    template_name='teams/six_create.html'
