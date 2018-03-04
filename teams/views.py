from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, View
import datetime
from django.utils import timezone
# team create forms
from teams.forms import TeamCreateForm
# team create invite forms
from .forms import TeamInviteForm, EditTeamProfileForm, ViewInviteForm
# import the team models
from teams.models import Team
# import the invite models
from teams.models import TeamInvite
from profiles.models import UserProfile


class MyInvitesListView(ListView):
    # show all the invites, and an accept or deny button.
    # check if the invite is expired.
    model = TeamInvite
    template_name = 'teams/my-invites.html'

    def get_queryset(self):
        # make sure that the invites are for the requested user
        return TeamInvite.objects.filter(user=self.request.user, active=True)


def InviteView(request, num):
    template_name = 'teams/invite.html'

    if request.method == "GET":
        form = ViewInviteForm()
        invite = TeamInvite.objects.get(id=num)
        return render(request, template_name, {'form': form, "invite": invite})
    if request.method == "POST":
        form = ViewInviteForm(request.POST)
        invite = TeamInvite.objects.get(id=num)
        #if form.is_valid():
        if form.data['accepted']:
                invite = TeamInvite.objects.get(id=num)
                invite.accepted = True
                invite.declined = False
                invite.expire = timezone.now()
                invite.active = False
                invite.save()
                messages.success(request, 'Accepted invite to '+str(invite.team))
                return redirect('/teams/my/')
        elif form.data['denied']:
                invite = TeamInvite.objects.get(id=num)
                invite.declined = True
                invite.accepted = False
                invite.expire = timezone.now()
                invite.active = False
                invite.save()
                messages.success(request, 'Declined invite to '+str(invite.team))
                return redirect('/teams/my/')
        #else:
            #messages.error(request, 'One or more fields was not valid. Please check your inputs.')
            #return render(request, template_name, {'form': form, 'invite': invite})


class MyTeamsListView(ListView):
    # list all the teams they are apart of
    # maybe list the role they have?
    model = Team
    template_name = 'teams/my-teams.html'

    def get_queryset(self):
        # TO DO switch the filter to the players field not just the founder field.
        if Team.objects.filter(founder=self.request.user):
            # TO DO switch the filter to the players field not just the founder field.
            return Team.objects.filter(founder=self.request.user)


def EditTeamView(request, pk):
        if request.method == 'POST':
            teamobj = Team.objects.get(team__founder=request.user.username)
            form = EditTeamProfileForm(request.POST, instance=teamobj)
            if form.is_valid():
                form.save()
                return redirect('/teams/' + str(request.user))
        else:
            teamobj = Team.objects.get(team__founder=request.user.username)
            form = EditTeamProfileForm(instance=teamobj)
            return render(request, 'teams/edit-team.html', {'form': form})


class MyTeamDetailView(DetailView):
    # show team info, allow them to invite users.
    model = Team
    # base team template all users can see, inside the template some permissions like viewing the edit team button
    # will be managed
    template_name = 'teams/team.html'
    form = TeamInviteForm

    def get_context_date(self, **kwargs):
        context = super(MyTeamDetailView, self).get_context_date(**kwargs)
        context['form'] = self.form
        return context

    def post(self,request, *args, **kwargs):
        self.form = TeamInviteForm(request.POST)
        if self.form.is_valid():
            self.form_valid(self.form)
            return HttpResponseRedirect(reverse('teams:detail', args=[self.kwargs['pk']]))
        return super(MyTeamDetailView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        invite = form.instance
        invite.inviter = self.request.inviter
        invite.user = self.request.user
        invite.team = self.request.team

    def get_queryset(self):
        # TO DO switch the filter to the players field not just the founder field.
        return Team.objects.filter(founder=self.request.user)


class TeamCreateView(CreateView):
    form_class = TeamCreateForm
    template_name = 'teams/create-team.html'

    def form_valid(self, form):
        Team = form.instance
        Team.founder = self.request.user
        Team.save()
        self.success_url = reverse('teams:detail', args=[Team.id])
        messages.success(self.request, 'Your Team has been created successfully')
        return super(TeamCreateView, self).form_valid(form)


class TeamInviteCreateView(View):
    template_name = 'teams/invite-player.html'
    form_class = TeamInviteForm

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            TeamInvite = form.instance
            TeamInvite.inviter = self.request.user
            TeamInvite.team = form.cleaned_data['team']
            try:
                invitee = UserProfile.objects.get(user__username=form.cleaned_data['user'])
            except:
                messages.error(request, "That isn't a valid user")
                return render(request, self.template_name, {'form':form})
            TeamInvite.user = invitee.user
            TeamInvite.expire = timezone.now() + datetime.timedelta(days=1)
            TeamInvite.save()
            messages.success(request, 'Sent invite successfully')
            return redirect('/teams/my/')

        return render(request, self.template_name, {'form': form})
