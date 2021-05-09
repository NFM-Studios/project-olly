import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.views.generic import ListView, DetailView, View
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from pages.models import OllySetting
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
    elif request.method == "POST":
        form = ViewInviteForm(request.POST)
        invite = TeamInvite.objects.get(id=num)
        if form.is_valid():
            accepted = form.cleaned_data['accepted']
            if form.cleaned_data['accepted'] == form.cleaned_data['denied']:
                messages.error(request, "Please select either accepted or denied, not both.")
                return render(request, template_name, {'form': form, 'invite': invite})
            if accepted:
                invite = TeamInvite.objects.get(id=num)
                invite.accepted = True
                invite.expire = timezone.now()
                invite.active = False
                invite.save()

                if invite.captain:
                    profile = UserProfile.objects.get(user=invite.user)
                    profile.captain_teams.add(invite.team)
                    profile.save()
                    invite.team.captain.add(invite.user)
                    invite.team.save()
                    messages.success(request, 'Successfully added the team to your profile as a captain')
                else:
                    profile = UserProfile.objects.get(user=invite.user)
                    profile.player_teams.add(invite.team)
                    profile.save()
                    messages.success(request, 'Successfully added the team to your profile as a player')
                    invite.team.players.add(invite.user)
                    invite.team.save()
                messages.success(request, 'Accepted invite to ' + str(invite.team.name))
                return redirect('teams:list')
            elif not accepted:
                invite = TeamInvite.objects.get(id=num)
                invite.delete()
                messages.success(request, 'Declined invite to ' + str(invite.team.name))
                return redirect('teams:list')
        else:
            messages.error(request, "An unknown error has occured")
            return redirect('teams:list')


def MyTeamsListView(request):
    profile = UserProfile.objects.get(user=request.user)
    return render(request, 'teams/team_list.html',
                  {'founder_teams': profile.founder_teams.all(), 'captain_teams': profile.captain_teams.all(),
                   'player_teams': profile.player_teams.all()})


def edit_team_view(request, pk):
    teamobj = get_object_or_404(Team, id=pk)
    profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = EditTeamProfileForm(request.POST, request.FILES, instance=teamobj)
        if profile.user in teamobj.captain.all() or profile.user == teamobj.founder:
            if form.is_valid():
                form.save()
                messages.success(request, 'Team successfully updated')
                return redirect(reverse('teams:detail', args=[pk]))
            else:
                messages.error(request, 'An unknown error has occured')
                return redirect(reverse('teams:detail', args=[pk]))
        else:
            messages.error(request, 'ERROR: You must be a captain or founder to update team info')
            return redirect('teams:detail', pk=teamobj.pk)
    else:
        if profile.user in teamobj.captain.all() or profile.user == teamobj.founder:
            form = EditTeamProfileForm(instance=teamobj)
            return render(request, 'teams/team_edit.html', {'form': form})
        else:
            messages.error(request, 'ERROR: You must be a captain or founder to update team info')
            return redirect('teams:detail', pk=teamobj.pk)


class MyTeamDetailView(DetailView):
    # show team info, allow them to invite users.
    model = Team
    # base team template all users can see, inside the template some permissions like viewing the edit team button
    # will be managed
    form = TeamInviteFormPost

    def get(self, request, pk):
        team = get_object_or_404(Team, id=pk)
        players = team.players.all()
        captains = team.captain.all()
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
            Q(captain__exact=self.request.user) | Q(founder=self.request.user) | Q(players__exact=self.request.user))


class TeamCreateView(View):
    form_class = TeamCreateForm

    def get(self, request):
        if OllySetting.objects.get(pk=1).can_create_team():
            pass
        else:
            messages.error(request, "An admin has disabled team creation")
            return redirect('teams:list')
        form = self.form_class()
        return render(request, 'teams/team_create.html', {'form': form})

    def post(self, request):
        if OllySetting.objects.get(pk=1).can_create_team():
            pass
        else:
            messages.error(request, "An admin has disabled team creation")
            return redirect('teams:list')
        form = self.form_class(request.POST)

        if form.is_valid():
            Team = form.instance
            if len(Team.name) < 5:
                messages.error(self.request, 'Your team name must be 5 or more characters')
                return redirect('teams:create')

            Team.founder = self.request.user
            profile = UserProfile.objects.get(user=request.user)
            Team.save()
            profile.founder_teams.add(Team)
            profile.save()
            messages.success(self.request, 'Your Team has been created successfully')
            return redirect('teams:detail', pk=Team.pk)


def get_invites(form):
    return TeamInvite.objects.filter(team=form.cleaned_data['team'])


class TeamInviteCreateView(View):
    template_name = 'teams/team_invite_player.html'
    form_class = TeamInviteFormGet

    def get(self, request):
        if OllySetting.objects.get(pk=1).can_invite():
            pass
        else:
            messages.error(request, "An admin has disabled team invite creation")
            return redirect('teams:list')
        form = self.form_class(request)
        return render(request, 'teams/team_invite_player.html', {'form': form})

    def post(self, request):
        if OllySetting.objects.get(pk=1).can_invite():
            pass
        else:
            messages.error(request, "An admin has disabled team invite creation")
            return redirect('teams:list')
        form = TeamInviteFormPost(request.POST)
        team = Team.objects.get(id=form.data['team'])
        invite = get_invites(form)
        captains = team.captain.all()
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
                #TODO remove try except
                try:
                    if form.data['captain']:
                        TeamInvite.captain = True
                except:
                    pass
                # lets send a notification
                TeamInvite.save()
                notif = UserProfile.objects.get(user=TeamInvite.user)
                temp = Notification(type='team', title="You've been invited to join a team",
                                    description="What are you waiting for? Someone needs you to join their team! "
                                                "View your team invites now!", link='teams:myinvitelist')

                temp.datetime = datetime.datetime.utcnow()
                temp.save()
                notif.notifications.add(temp)
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
                    email.send(fail_silently=True)
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
            if request.user in team.players.all():
                team.players.remove(request.user)
                messages.success(request, 'Successfully removed you from the players role')
            if request.user in team.captain.all():
                team.captain.remove(request.user)
                messages.success(request, 'Successfully removed you from the captain role')
            if request.user is team.founder.all():
                # founders cannot leave their team. they must delete the team
                messages.error(request,
                               'You cannot leave the team you founded, you can only delete it.')
            if not (request.user in team.players.all()) or not (request.user in team.captain.all()) or not (
                    request.user is team.founder.all()):
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
        if request.user == team.founder or request.user in team.captain.all():
            form = RemoveUserForm(request, pk)
            return render(request, 'teams/team_remove_user.html', {'form': form, 'pk': pk})
        else:
            messages.error(request, "Only the team's founder can remove users")
            return redirect('teams:detail', pk)

    def post(self, request, pk):
        team = Team.objects.get(id=pk)
        if request.user == team.founder or request.user in team.captain.all():
            form = RemovePlayerFormPost(request.POST)
            # invite = TeamInvite.objects.get(id=form.data['remove'])
            user = form.data['remove']
            player = UserProfile.objects.get(user=user)
            if player.user == team.founder:
                messages.error(request, "You cannot remove the Team founder from the team")
                return redirect('teams:detail', pk=pk)
            else:
                team.players.remove(player.user)
                team.save()
                messages.success(request, 'Removed user %s from team' % player)
                return redirect('teams:detail', pk=pk)

        else:
            messages.error(request, "Only the team's founder or a captain can remove users")
            return redirect('teams:detail', pk)


def add_founder_as_captain(request, pk):
    team = Team.objects.get(pk=pk)
    if team != None:
        if request.user == team.founder:
            # its the right guy
            if team.founder not in team.captain.all():
                team.captain.add(request.user)
                # mtm fields don't need to be saved :thinking:
                # team.captain.save()
                messages.success(request, "You were added as a captain to the team")
                return redirect('teams:detail', pk=pk)
            else:
                messages.error(request, "You are already a captain on your team")
                return redirect('teams:detail', pk=pk)
        else:
            messages.error(request, "Error, You are not the founder of this team")
            return redirect('teams:detail', pk=pk)
    else:
        messages.error(request, "Error finding the correct team")
        return redirect('teams:detail', pk=pk)


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
