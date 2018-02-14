from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView
#team create forms
from teams.forms import TeamCreateForm
#team create invite forms
from teams.forms import TeamInviteForm, CaptainInviteForm
#import the team models
from teams.models import Team
#import the invite models
from teams.models import TeamInvite, CaptainInvite

class MyInvitesListView(ListView):
    # show all the invites, and an accept or deny button.
    # check if the invite is expired.
    model = TeamInvite
    template_name = 'teams/my-invites.html'

    def get_queryset(self):
        #make sure that the invites are for the requested user
        return TeamInvite.objects.filter(user=self.request.user)



class MyTeamsListView(ListView):
# list all the teams they are apart of
# maybe list the role they have?
    model = Team
    template_name='teams/my-teams.html'

    def get_queryset(self):
        if(Team.objects.filter(players=self.request.user)):
            #maybe? filter items where the mtm field contains one of the users.
            return Team.objects.filter(players__contains=self.requst.user)




class MyTeamDetailView(DetailView):
#show team info, allow them to invite users.
    model = Team
    #base team template all users can see, inside the template some permissions like viewing the edit team button
    # will be managed
    template_name = 'teams/team.html'
    form = TeamInviteCreateForm

    #def invite(self, request, *args, **kwargs):
    #    self.form=TeamInviteCreateForm(request.POST)

class TeamInviteCreateView(CreateView):
#allow the person to create an invite for there team
    form_class = TeamInviteCreateForm
    template_name = 'teams/invite-player.html'

    def form_valid(self, form):
        TeamInvite = form.instance
        TeamInvite.inviter = self.request.user
        TeamInvite.save()
        self.success_url = reverse('teams:detail', args=[TeamInvite.id])
        messages.success(self.request, 'Your invite has been successfully sent')
        return super(TeamInviteCreateView, self).form_valid(form)


class CaptainInviteCreateView(CreateView):
    form_class = CaptainInviteForm
    template_name='teams/captain-invite.html'
    form = CaptainInviteCreateForm()

    def form_valid(self, form):
        CaptainInvite = form.instance
        CaptainInvite.inviter = self.request.user
        CaptainInvite.team =
        CaptainInvite.user =

class TeamCreateView(CreateView):
    form_class=TeamCreateForm
    template_name='teams/create-team.html'

    def form_valid(self, form):
        Team = form.instance
        Team.founder = self.request.user
        Team.save()
        self.success_url = reverse('teams:detail', args=[Team.id])
        messages.success(self.request, 'Your Team has been created successfully')
        return super(TeamCreateView, self).form_valid(form)
