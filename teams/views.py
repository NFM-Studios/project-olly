from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, View
from django.contrib.auth.models import User
import datetime
from django.utils import timezone
# team create forms
from teams.forms import TeamCreateForm
# team create invite forms
from .forms import TeamInviteForm, EditTeamProfileForm, ViewInviteForm, LeaderboardSortForm
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
        try:
            accepted = form.data['accepted']
        except:
            accepted = 'off'
        if form.is_valid():
            try:
                if form.data['accepted'] == form.data['denied']:
                    messages.error(request, "Only select accepted or denied, not both.")
                    return render(request, template_name, {'form': form, 'invite': invite})
            except:
                if accepted == 'on':
                    invite = TeamInvite.objects.get(id=num)
                    invite.accepted = True
                    invite.expire = timezone.now()
                    invite.active = False
                    invite.save()
                    messages.success(request, 'Accepted invite to '+str(invite.team.name))
                    return redirect('/teams/')
                elif accepted == 'off':
                    invite = TeamInvite.objects.get(id=num)
                    invite.declined = True
                    invite.expire = timezone.now()
                    invite.active = False
                    invite.save()
                    messages.success(request, 'Declined invite to '+str(invite.team.name))
                    return redirect('/teams/')


class MyTeamsListView(ListView):
    # list all the teams they are apart of
    # maybe list the role they have?
    model = Team
    template_name = 'teams/my-teams.html'

    def get(self, request):
        team_list = TeamInvite.objects.filter(user=self.request.user, accepted=True)
        return render(request, self.template_name, {'team_list': team_list})

    def get_queryset(self, **kwargs):
        # TO DO switch the filter to the players field not just the founder field.
        if TeamInvite.objects.filter(user=self.request.user, accepted=True):
            # TO DO switch the filter to the players field not just the founder field.
            return TeamInvite.objects.filter(user=self.request.user, accepted=True)


def EditTeamView(request, pk):
        if request.method == 'POST':
            teamobj = Team.objects.get(team__founder=request.user.username)
            form = EditTeamProfileForm(request.POST, instance=teamobj)
            if form.is_valid():
                form.save()
                return redirect('/teams/' + str(request.user))
        else:
            teamobj = Team.objects.get(id=pk)
            form = EditTeamProfileForm(instance=teamobj)
            return render(request, 'teams/edit-team.html', {'form': form})


class MyTeamDetailView(DetailView):
    # show team info, allow them to invite users.
    model = Team
    # base team template all users can see, inside the template some permissions like viewing the edit team button
    # will be managed
    template_name = 'teams/team.html'
    form = TeamInviteForm

    def get(self, request, pk):
        team = Team.objects.get(id=pk)
        players = TeamInvite.objects.filter(team=team, accepted=True)
        return render(request, self.template_name, {'team': team, 'players': players})

    def get_context_date(self, **kwargs):
        context = super(MyTeamDetailView, self).get_context_date(**kwargs)
        context['form'] = self.form
        return context

    def post(self, request, *args, **kwargs):
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
        invite = TeamInvite()
        invite.expire = timezone.now()
        invite.user = self.request.user
        invite.captain = 'founder'
        invite.accepted = True
        invite.inviter = self.request.user
        invite.inviter_id = self.request.user.id
        invite.team_id = Team.id
        invite.save()
        self.success_url = reverse('teams:detail', args=[Team.id])
        messages.success(self.request, 'Your Team has been created successfully')
        return super(TeamCreateView, self).form_valid(form)


def get_invites(form):
    return TeamInvite.objects.filter(team=form.data['team'])


class TeamInviteCreateView(View):
    template_name = 'teams/invite-player.html'
    form_class = TeamInviteForm

    def get(self, request):
        form = self.form_class(request)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        team = Team.objects.get(id=form.data['team'])
        invite = get_invites(form)
        captains = invite.filter(captain='captain')
        x = {}
        for captain in captains:
            x[captain] = str(captain.user.username)
        if (request.user == team.founder) or (request.user.username in x.values()):
            try:
                invitee = UserProfile.objects.get(user__username=form.data['user'])
            except:
                messages.error(request, "That isn't a valid user")
                return render(request, self.template_name, {'form': form})
            query = invite.filter(user=invitee.user, team=form.data['team'])
            if query.exists():
                messages.error(request, "That user already has been invited to this team")
                return redirect('/teams/')
            else:
                TeamInvite = form.instance
                TeamInvite.inviter = self.request.user
                TeamInvite.team = team
                TeamInvite.user = invitee.user
                TeamInvite.expire = timezone.now() + datetime.timedelta(days=1)
                TeamInvite.captain = form.data['captain']
                TeamInvite.save()
                messages.success(request, 'Sent invite successfully')
                return redirect('/teams/')

        else:
            messages.error(request, "You must be a captain or the founder to invite")
            return redirect('/teams/')


class LeaderboardView(View):
    template_name = 'teams/leaderboard.html'
    form_class = LeaderboardSortForm

    def get(self, request, **kwargs):
        user_list = UserProfile.objects.order_by('user__username')  # sort by username default
        form = self.form_class(None)
        return render(request, self.template_name, {'user_list': user_list, 'form': form})

    def post(self, request, **kwargs):
        form = self.form_class(request.POST)
        xp_asc = False
        xp_desc = False
        trophies_asc = False
        trophies_desc = False
        try:
            if form.data['sort_xp_asc']:
                xp_asc = True
                xp_desc = False
                trophies_asc = False
                trophies_desc = False
        except:
            try:
                if form.data['sort_xp_desc']:
                    xp_desc = True
                    xp_asc = False
                    trophies_asc = False
                    trophies_desc = False
            except:
                try:
                    if form.data['sort_trophies_asc']:
                        trophies_asc = True
                        xp_desc = False
                        xp_asc = False
                        trophies_desc = False
                except:
                    try:
                        if form.data['sort_trophies_desc']:
                            trophies_desc = True
                            xp_desc = False
                            trophies_asc = False
                            xp_desc = False
                    except:
                        user_list = UserProfile.objects.order_by('user__username')
                        messages.error(request, "You have to select an option to sort")
                        return render(request, self.template_name, {'user_list': user_list, 'form': self.form_class(None)})
        if xp_asc:
            user_list = UserProfile.objects.order_by('xp')
            messages.success(request, "Sorted by ascending XP")
            return render(request, self.template_name, {'user_list': user_list, 'form': self.form_class(None)})
        elif xp_desc:
            user_list = UserProfile.objects.order_by('-xp')
            messages.success(request, "Sorted by descending XP")
            return render(request, self.template_name, {'user_list': user_list, 'form': self.form_class(None)})
        elif trophies_asc:
            user_list = UserProfile.objects.order_by('num_trophies')
            messages.success(request, "Sorted by ascending number of trophies")
            return render(request, self.template_name, {'user_list': user_list, 'form': self.form_class(None)})
        elif trophies_desc:
            user_list = UserProfile.objects.order_by('-num_trophies')
            messages.success(request, "Sorted by descending number of trophies")
            return render(request, self.template_name, {'user_list': user_list, 'form': self.form_class(None)})
