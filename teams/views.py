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
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

from matches.models import Match
from profiles.models import UserProfile, Notification
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
        teaminvite_list = TeamInvite.objects.filter(Q(user=self.request.user, active=True))
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
                    team = invite.team
                    if invite.captain:
                        team.captains.add(request.user)
                    else:
                        team.players.add(request.user)
                    messages.success(request, 'Accepted invite to ' + str(invite.team.name))
                    return redirect('teams:list')
                elif accepted == 'off':
                    invite = TeamInvite.objects.get(id=num)
                    invite.delete()
                    messages.success(request, 'Declined invite to ' + str(invite.team.name))
                    return redirect('teams:list')


class MyTeamsListView(ListView):
    # list all the teams they are apart of
    # maybe list the role they have?
    model = Team

    def get(self, request):
        team_list = Team.objects.filter(
            Q(captains__exact=request.user) | Q(founder=request.user) | Q(players__exact=request.user))
        return render(request, 'teams/team_list.html', {'team_list': team_list})

    def get_queryset(self, **kwargs):
        return Team.objects.filter(
            Q(captains__exact=self.request.user) | Q(founder=self.request.user) | Q(players__exact=self.request.user))


def edit_team_view(request, pk):
    if request.method == 'POST':
        teamobj = get_object_or_404(Team, id=pk)
        form = EditTeamProfileForm(request.POST, request.FILES, instance=teamobj)
        if request.user not in teamobj.captains or request.user is not teamobj.founder:
            messages.error(request, 'ERROR: You must be a captain or founder update team info')
            return redirect('teams:detail', pk=teamobj.pk)
        if form.is_valid():
            form.save()
            messages.success(request, 'Team successfully updated')
            return redirect(reverse('teams:detail', args=[pk]))
        else:
            messages.error(request, 'An unknown error has occured')
            return redirect(reverse('teams:detail', args=[pk]))
    else:
        teamobj = Team.objects.get(id=pk)
        form = EditTeamProfileForm(instance=teamobj)
        return render(request, 'teams/team_edit.html', {'form': form})


class MyTeamDetailView(DetailView):
    # show team info, allow them to invite users.
    model = Team
    # base team template all users can see, inside the template some permissions like viewing the edit team button
    # will be managed
    form = TeamInviteFormPost

    def get(self, request, pk):
        team = get_object_or_404(Team, id=pk)
        players = team.players.all()
        captains = team.captains.all()
        matches_ = Match.objects.filter(awayteam_id=team.id)
        matches__ = Match.objects.filter(hometeam_id=team.id)
        matches = matches_ | matches__
        if not request.user.is_anonymous:
            user = UserProfile.objects.get(user__username=request.user.username)
            return render(request, 'teams/team_detail.html',
                          {'team': team, 'players': players, 'pk': pk, 'matches': matches, 'captains': captains})
        else:
            return render(request, 'teams/team_detail.html',
                          {'team': team, 'players': players, 'pk': pk, 'matches': matches, 'captains': captains})

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
        return Team.objects.filter(
            Q(captains__exact=self.request.user) | Q(founder=self.request.user) | Q(players__exact=self.request.user))


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

            messages.success(self.request, 'Your Team has been created successfully')
            return redirect('teams:detail', pk=Team.pk)


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
        captains = team.captains.all()
        if (request.user == team.founder) or (request.user.username in captains):
            try:
                invitee = UserProfile.objects.get(user__username=form.data['user'])
            except:
                messages.error(request, "That isn't a valid user")
                return render(request, 'teams/team_invite_player.html', {'form': form})
            query = invite.filter(user=invitee.user, team=form.data['team'])
            if query.exists():
                messages.error(request, "That user has already been invited to this team")
                return redirect('teams:detail', pk=team.pk)
            else:
                TeamInvite = form.instance
                TeamInvite.inviter = self.request.user
                TeamInvite.team = team
                TeamInvite.user = invitee.user
                TeamInvite.expire = timezone.now() + datetime.timedelta(days=1)
                if form.data['captain']:
                    TeamInvite.captain = True
                TeamInvite.save()
                # lets send a notification
                notif = UserProfile.objects.get(user=TeamInvite.user)
                temp = Notification(type='team', title="You've been invited to join a team",
                                    description="What are you waiting for? Someone needs you to join their team! "
                                                "View your team invites now!", link='teams:myinvitelist')

                temp.datetime = datetime.datetime.utcnow()
                temp.save()
                notif = notif.notifications.add(temp)
                notif.save()
                messages.success(request, 'Successfully notified user')
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
                return redirect('teams:list')

        else:
            messages.error(request, "You must be a captain or the founder to invite")
            return redirect('teams:list')


class LeaveTeamView(View):
    template_name = 'teams/team_leave.html'
    form_class = LeaveTeamForm

    def get(self, request, pk):
        form = self.form_class()
        team = Team.objects.get(id=pk)
        return render(request, 'teams/team_leave.html', {'form': form, 'team': team})

    def post(self, request, pk):
        form = self.form_class(request.POST)
        if form.data['confirmed']:
            try:
                team = Team.objects.get(pk=pk)
            except ObjectDoesNotExist:
                messages.error(request, 'Team cannot be found')
                return redirect('teams:list')
            if request.user in team.players:
                team.players.remove(request.user)
                messages.success(request, 'Successfully removed you from the players role')
            if request.user in team.captains:
                team.captains.remove(request.user)
                messages.success(request, 'Successfully removed you from the captain role')
            if request.user is team.founder:
                # founders cannot leave their team. they must delete the team
                messages.error(request,
                               'You cannot leave the team you founded, you can only delete it.')
            if not (request.user in team.players) or not (request.user in team.captains) or not (
                    request.user is team.founder):
                messages.error(request, "You don't appear to be on this team")
                return redirect('teams:detail', pk=pk)
            return redirect('teams:list')
        else:
            messages.error(request,
                           "You submitted without confirming that you wanted to leave, redirecting to team detail")
            return redirect('teams:detail', pk=pk)


class RemoveUserView(View):
    template_name = 'teams/team_remove_user.html'

    def get(self, request, pk):
        team = Team.objects.get(id=pk)
        if request.user == team.founder or request.user in team.captains:
            form = RemoveUserForm(request, pk)
            return render(request, 'teams/team_remove_user.html', {'form': form, 'pk': pk})
        else:
            messages.error(request, "Only the team's founder can remove users")
            return redirect('teams:detail', pk)

    def post(self, request, pk):
        team = Team.objects.get(id=pk)
        if request.user == team.founder or request.user in team.captains:
            form = RemovePlayerFormPost(request.POST)
            # invite = TeamInvite.objects.get(id=form.data['remove'])
            player = UserProfile.objects.get(form.data['remove'])
            if player == team.founder:
                messages.error(request, "You cannot remove the Team founder from the team")
                return redirect('teams:list')
            else:
                team.players.remove(player)
                team.save()
                messages.success(request, 'Removed user %s from team' % player)

        else:
            messages.error(request, "Only the team's founder or a captain can remove users")
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
                    try:
                        invites = list(TeamInvite.objects.filter(team=team))
                        for invite in invites:
                            invite.delete()
                    except:
                        messages.error(request, "Warning: Couldn't delete team invites")
                    messages.success(request, 'Dissolved team %s' % team)
                    team.delete()
                    return redirect('teams:list')
                else:
                    messages.warning(request, "You didn't confirm that you wanted to dissolve the team")
                    return redirect('teams:detail', pk)
        else:
            messages.error(request, "Only the team's founder can dissolve the team")
            return redirect('teams:detail', pk)
