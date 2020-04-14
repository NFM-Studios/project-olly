import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.views.generic import ListView, DetailView, View

from matches.models import Match
from profiles.models import UserProfile
# team create forms
from teams.forms import TeamCreateForm
# import the team models
from teams.models import Team
# import the invite models
from teams.models import TeamInvite
# team create invite forms
from .forms import TeamInviteFormGet, TeamInviteFormPost, EditTeamProfileForm, ViewInviteForm, LeaveTeamForm, \
    RemovePlayerFormPost, RemoveUserForm, DissolveTeamForm


class MyInvitesListView(ListView):
    # show all the invites, and an accept or deny button.
    # check if the invite is expired.
    model = TeamInvite

    def get(self, request):
        teaminvite_list = TeamInvite.objects.filter(user=self.request.user, active=True)
        return render(request, 'teams/team_invite_list.html', {'teaminvite_list': teaminvite_list})

    def get_queryset(self):
        # make sure that the invites are for the requested user
        return TeamInvite.objects.filter(user=self.request.user, active=True)


def invite_view(request, num):
    template_name = 'teams/team_invite_detail.html'

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

    def get(self, request):
        team_list = TeamInvite.objects.filter(user=self.request.user, accepted=True)
        return render(request, 'teams/team_list.html', {'team_list': team_list})

    def get_queryset(self, **kwargs):
        # TO DO switch the filter to the players field not just the founder field.
        if TeamInvite.objects.filter(user=self.request.user, accepted=True):
            # TO DO switch the filter to the players field not just the founder field.
            return TeamInvite.objects.filter(user=self.request.user, accepted=True)


def edit_team_view(request, pk):
    if request.method == 'POST':
        teamobj = get_object_or_404(Team, id=pk)
        form = EditTeamProfileForm(request.POST, request.FILES, instance=teamobj)
        if form.is_valid():
            #teamobj.about_us = form.data['about_us']
            #teamobj.website = form.data['website']
            #teamobj.twitter = form.data['twitter']
            #teamobj.twitch = form.data['twitch']
            #teamobj.country = form.data['country']
            #teamobj.image = form.data['image']
            #teamobj.save()
            form.save()
            messages.success(request, 'Team successfully updated')
            return redirect(reverse('teams:detail', args=[pk]))
        else:
            messages.error(request, 'An unknown error has occured')
            return redirect(reverse('teams:detail', args=[pk]))
    else:
        teamobj = Team.objects.get(id=pk)
        form = EditTeamProfileForm(instance=teamobj)
        return render(request, 'team/team_edit.html', {'form': form})


class MyTeamDetailView(DetailView):
    # show team info, allow them to invite users.
    model = Team
    # base team template all users can see, inside the template some permissions like viewing the edit team button
    # will be managed
    form = TeamInviteFormPost

    def get(self, request, pk):
        team = get_object_or_404(Team, id=pk)
        players = TeamInvite.objects.filter(team=team, accepted=True)
        up = []
        for player in players:
            up.append(UserProfile.objects.get(user__username=player))
        matches_ = Match.objects.filter(awayteam_id=team.id)
        matches__ = Match.objects.filter(hometeam_id=team.id)
        matches = matches_ | matches__
        if not request.user.is_anonymous:
            user = UserProfile.objects.get(user__username=request.user.username)
            if not user.xbl_verified:
                messages.warning(request, "Xbox Live is not verified")
            if not user.psn_verified:
                messages.warning(request, "PSN is not verified")
            return render(request, 'teams/team_detail.html', {'team': team, 'players': players, 'up':up,'pk': pk, 'matches': matches})
        else:
            return render(request, 'teams/team_detail.html', {'team': team, 'players': players, 'up':up, 'pk': pk, 'matches': matches})

    def get_context_date(self, **kwargs):
        context = super(MyTeamDetailView, self).get_context_date(**kwargs)
        context['form'] = self.form
        return context

    def post(self, request, *args, **kwargs):
        self.form = TeamInviteFormPost(request.POST)
        if self.form.is_valid():
            self.form_valid(self.form)
            if not request.user.xbl_verified:
                messages.warning(request, "Xbox Live is not verified")
            if not request.user.psn_verified:
                messages.warning(request, "PSN is not verified")
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


class TeamCreateView(View):
    form_class = TeamCreateForm

    def get(self, request):
        form = self.form_class()
        return render(request, 'teams/team_create.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            Team = form.instance
            if len(Team.name) < 5:
                messages.error(self.request, 'Your team name must be 5 or more characters')
                return redirect('teams:create')

            Team.founder = self.request.user
            Team.save()
            invite = TeamInvite()
            invite.expire = timezone.now()
            invite.user = self.request.user
            invite.captain = 'founder'
            invite.hasPerms = True
            invite.accepted = True
            invite.inviter = self.request.user
            invite.inviter_id = self.request.user.id
            invite.team_id = Team.id
            invite.save()

            messages.success(self.request, 'Your Team has been created successfully')
            return redirect('teams:list')


def get_invites(form):
    return TeamInvite.objects.filter(team=form.data['team'])


class TeamInviteCreateView(View):
    template_name = 'teams/team_invite_player.html'
    form_class = TeamInviteFormGet

    def get(self, request):
        form = self.form_class(request)
        return render(request, 'teams/team_invite_player.html', {'form': form})

    def post(self, request):
        form = TeamInviteFormPost(request.POST)
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
                return render(request, 'teams/team_invite_player.html', {'form': form})
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
                if form.data['captain'] == 'captain' or form.data['captain'] == 'founder':
                    TeamInvite.hasPerms = True
                TeamInvite.save()
                if invitee.email_enabled:
                    current_site = get_current_site(request)
                    mail_subject = settings.SITE_NAME + ": You've been invited to a team!"
                    message = render_to_string('teams/invite_email.html', {
                        'user': invitee.user.username,
                        'site': settings.SITE_NAME,
                        'domain': current_site.domain,
                        'pk': TeamInvite.pk
                    })
                    email = EmailMessage(
                        mail_subject, message, from_email=settings.FROM_EMAIL, to=[invitee.user.email]
                    )
                    email.send()
                messages.success(request, 'Sent invite successfully')
                return redirect('/teams/')

        else:
            messages.error(request, "You must be a captain or the founder to invite")
            return redirect('/teams/')


class LeaveTeamView(View):
    template_name = 'teams/team_leave.html'
    form_class = LeaveTeamForm

    def get(self, request, pk):
        form = self.form_class()
        team = Team.objects.get(id=pk)
        return render(request, 'teams/team_leave.html', {'form': form, 'team': team})

    def post(self, request, pk):
        form = self.form_class(request.POST)
        try:
            if form.data['confirmed']:
                invite = TeamInvite.objects.get(user=request.user, team_id=pk)
                try:
                    invite.delete()
                    messages.success(request, "Left team")
                    invites = TeamInvite.objects.filter(team_id=pk)
                    if not invites.exists():
                        team = Team.objects.get(id=pk)
                        team.delete()
                        messages.success(request, 'Deleted team due to the last user leaving')
                    return redirect('teams:list')
                except:
                    messages.error(request, "You don't appear to be on this team")
                    return redirect('teams:detail', pk=pk)
        except:
            messages.error(request, "You submitted without confirming that you wanted to leave, redirecting to team detail")
            return redirect('teams:detail', pk=pk)


class RemoveUserView(View):
    template_name = 'teams/team_remove_user.html'

    def get(self, request, pk):
        team = Team.objects.get(id=pk)
        if request.user == team.founder:
            form = RemoveUserForm(request, pk)
            return render(request, 'teams/team_remove_user.html', {'form': form, 'pk': pk})
        else:
            messages.error(request, "Only the team's founder can remove users")
            return redirect('teams:detail', pk)

    def post(self, request, pk):
        team = Team.objects.get(id=pk)
        if request.user == team.founder:
            form = RemovePlayerFormPost(request.POST)
            invite = TeamInvite.objects.get(id=form.data['remove'])
            messages.success(request, 'Removed user %s from team' % invite)
            invite.delete()
            invites = TeamInvite.objects.filter(team=team)
            if not invites.exists():
                messages.warning(request, "Last user in team removed, team deleted")
                team.delete()
                return redirect('teams:list')
            else:
                return redirect('teams:detail', pk)
        else:
            messages.error(request, "Only the team's founder can remove users")
            return redirect('teams:detail', pk)


class DissolveTeamView(View):
    template_name = 'teams/team_dissolve.html'

    def get(self, request, pk):
        team = Team.objects.get(id=pk)
        if request.user == team.founder:
            form = DissolveTeamForm(request, pk)
            return render(request, 'teams/team_dissolve.html', {'form': form, 'pk': pk})
        else:
            messages.error(request, "Only the team's founder can dissolve the team")
            return redirect('teams:detail', pk)

    def post(self, request, pk):
        team = Team.objects.get(id=pk)
        if request.user == team.founder:
            form = DissolveTeamForm(request.POST)
            if form.is_valid():
                if form.cleaned_data['confirmed']:
                    team = Team.objects.get(id=pk)
                    invites = list(TeamInvite.objects.filter(team=team))
                    for invite in invites:
                        invite.delete()
                    messages.success(request, 'Dissolved team %s' % team)
                    team.delete()
                    return redirect('teams:list')
                else:
                    messages.warning(request, "You didn't confirm that you wanted to dissolve the team")
                    return redirect('teams:detail', pk)
        else:
            messages.error(request, "Only the team's founder can remove users")
            return redirect('teams:detail', pk)
