import datetime
import pytz
from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import View

from profiles.models import UserProfile
from store.models import deduct_credits, give_credits
from teams.models import Team
from .forms import SingleEliminationTournamentJoinGet, SingleEliminationTournamentJoinPost, \
    SingleEliminationTournamentSort, SingleTournamentLeaveForm
from .models import SingleTournamentRound, SingleEliminationTournament, SingleTournamentTeam


class List(View):
    form_class = SingleEliminationTournamentSort

    def get(self, request):
        form = self.form_class(None)
        tournament_list = SingleEliminationTournament.objects.all().filter(active=True)
        return render(request, 'singletournaments/singletournament_list.html',
                      {'tournament_list': tournament_list, 'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if not form.is_valid():
            tournament_list = SingleEliminationTournament.objects.all().filter(active=True)
            return render(request, 'singletournaments/singletournament_list.html',
                          {'tournament_list': tournament_list, 'form': form})
        platform = form.cleaned_data['platform']
        game = form.cleaned_data['game']

        if game == 'all':
            tournament_list_ = SingleEliminationTournament.objects.all()
        else:
            tournament_list_ = SingleEliminationTournament.objects.filter(game=game)

        if platform == 'all':
            tournament_list1 = SingleEliminationTournament.objects.all()
        else:
            tournament_list1 = SingleEliminationTournament.objects.filter(platform=platform)

        tournament_list = tournament_list1 & tournament_list_
        return render(request, 'singletournaments/singletournament_list.html',
                      {'tournament_list': tournament_list, 'form': form})


class SingleTournamentJoin(View):

    def get(self, request, pk):
        # teaminvites = TeamInvite.objects.filter(user_id=request.user.id, hasPerms=True)
        profile = UserProfile.objects.get(user=request.user)
        teams = profile.founder_teams.all() | profile.captain_teams.all()
        tournament = get_object_or_404(SingleEliminationTournament, id=pk)
        if teams.count() != 0:
            form = SingleEliminationTournamentJoinGet(request)
            return render(request, 'singletournaments/singletournament_join.html',
                          {'form': form, 'tournament': tournament})
        else:
            messages.error(request, message="You aren't a captain or founder of any team!")
            return redirect('singletournaments:list')

    def post(self, request, pk):
        form = SingleEliminationTournamentJoinPost(request.POST)
        profile = UserProfile.objects.get(user=request.user)
        if not form.is_valid():
            messages.error(request, message="Please select a valid team to join with")
            return redirect('singletournaments:list')
        team = form.cleaned_data['teams']
        if team in profile.captain_teams.all() or team in profile.founder_teams.all():
            # good to go
            pass
        else:
            messages.error(request, message="You aren't a captain or founder of this team")
            return redirect('singletournaments:list')

        tournament = SingleEliminationTournament.objects.get(id=self.kwargs['pk'])
        if tournament.teamformat == 0:
            players = 1
        elif tournament.teamformat == 1:
            players = 2
        elif tournament.teamformat == 2:
            players = 3
        elif tournament.teamformat == 3:
            players = 4
        elif tournament.teamformat == 4:
            players = 5
        elif tournament.teamformat == 5:
            players = 6
        else:
            messages.error(request, "Tournament minimum player error-unable to join tournament")
            return redirect('singletournaments:detail', pk=tournament.pk)
        # team = Team.objects.get(id=int(form.data['teams']))
        # users = TeamInvite.objects.filter(team=form.data['teams'], accepted=True)
        registered_teams = tournament.teams.all()
        teameligible = False
        now = timezone.now()

        if tournament.bracket_generated:
            messages.error(request, "The bracket has already been generated for this tournament, new teams aren't "
                                    "permitted")
            return redirect('singletournaments:list')

        # registration is allowed if an admin has manually opened it
        # (allow_register), or if we are within the registration window
        if not tournament.allow_register:
            if tournament.open_register >= now:
                messages.error(request, 'Registration for this tournament is not open yet')
                return redirect('singletournaments:list')

            if tournament.close_register <= now:
                messages.error(request, 'Registration for this tournament is closed already')
                return redirect('singletournaments:list')

        if registered_teams.count() >= tournament.size:
            messages.error(request, "This tournament is full")
            return redirect('singletournaments:list')
        for player in team.players.all():
            user = UserProfile.objects.get(user=player)
            # logic like below allows for verification of xbl/psn/steam accounts linked
            """if not user.xbl_verified and tournament.platform == 1:
                teameligible = False
                messages.error(request, "One or more users does not have Xbox Live set")
                return redirect('teams:list')
            elif not user.psn_verified and tournament.platform == 0:
                teameligible = False
                messages.error(request, "One or more users does not have PSN set")
                return redirect('teams:list')"""
            if int(user.credits) < int(tournament.req_credits):
                teameligible = False
                messages.error(request, "One or more players does not have enough credits")
                return redirect('teams:list')
            else:
                teameligible = True
            if not teameligible:
                messages.error(request, "Not all members of your team are eligible to join")
        member_count = team.players.count() + team.captain.count() + (1 if team.founder is not None else 0)
        if member_count <= players:
            teameligible = False
            messages.error(request, "Your team does not have enough people to play in this tournament")
        if not teameligible:
            messages.error(request, "There was an issue with team eligibility for this tournament")
            return redirect('teams:list')
        if tournament.teams.filter(pk=team.pk).exists():
            messages.error(request, message="This team is already in this tournament")
            return redirect('singletournaments:list')
        # loop through every user on the team trying to join - see if they're a player/founder/captain
        # on any other team thats already registered
        for user in team.players.all():
            for otherteam in tournament.teams.all():
                for player in otherteam.players.all():
                    if user == player:
                        messages.error(request, "There is overlap between users in teams in the tournament")
                        return redirect('singletournaments:list')
                for captain in otherteam.captain.all():
                    if user == captain:
                        messages.error(request, "There is overlap between users in teams in the tournament")
                        return redirect('singletournaments:list')
                if user in otherteam.captain.all():
                    messages.error(request, "There is overlap between users in teams in the tournament")
                    return redirect('singletournaments:list')

        with transaction.atomic():
            tournament.teams.add(team)
            deduct_credits(request.user, tournament.req_credits)
            tournament_team = SingleTournamentTeam(team_id=team.id, tournament_id=tournament.id)
            tournament_team.save()
        messages.success(request, message="Joined tournament")
        return redirect('singletournaments:list')


class SingleTournamentLeave(View):
    def get(self, request, pk):
        form = SingleTournamentLeaveForm()
        return render(request, 'singletournaments/singletournament_leave.html', {'form': form})

    def post(self, request, pk):
        form = SingleTournamentLeaveForm(request.POST)
        tournament = SingleEliminationTournament.objects.filter(id=pk)
        user_teams = Team.objects.filter(id__in=tournament.values('teams'), founder=request.user)
        if not user_teams.exists():
            messages.error(request, "You are not in this tournament")
            return redirect('singletournaments:list')
        else:
            tournament = SingleEliminationTournament.objects.get(id=pk)
            if not tournament.bracket_generated:
                if not form.is_valid():
                    messages.error(request, "Invalid form submission")
                    return redirect('singletournaments:leave', pk=pk)
                if not form.cleaned_data['confirm']:
                    messages.error(request, "You submitted without confirming that you wanted to leave")
                    return redirect('singletournaments:leave', pk=pk)
                else:
                    user_team = tournament.teams.filter(founder=request.user).first()
                    if user_team is None:
                        messages.error(request, "You are not in this tournament")
                        return redirect('singletournaments:list')
                    team = SingleTournamentTeam.objects.get(team_id=user_team.id, tournament=tournament)
                    team.delete()
                    tournament.teams.remove(user_team)
                    team_users = set(user_team.players.all())
                    team_users.update(user_team.captain.all())
                    if user_team.founder is not None:
                        team_users.add(user_team.founder)
                    for user in team_users:
                        give_credits(user=user, num=tournament.req_credits)
                    messages.success(request, "Gave %s credits to %s users" % (tournament.req_credits, len(team_users)))
                    messages.success(request, "Left tournament %s" % tournament.name)
                    return redirect('singletournaments:list')
            else:
                messages.error(request, "The bracket has been generated already, you cannot leave the tournament")
                return redirect('singletournaments:detail', pk=pk)


class SingleTournamentDetail(View):

    def get(self, request, **kwargs):
        pk = self.kwargs['pk']
        tournament = get_object_or_404(SingleEliminationTournament, id=pk)
        ruleset = tournament.ruleset
        teams = tournament.teams.all()
        return render(request, 'singletournaments/singletournament_detail.html',
                      {'pk': pk, 'tournament': tournament, 'ruleset': ruleset, 'teams': teams})


class SingleTournamentTeamsList(View):

    def get(self, request, **kwargs):
        pk = self.kwargs['pk']
        tournament = SingleEliminationTournament.objects.get(id=pk)
        teams = tournament.teams.all()
        return render(request, 'singletournaments/singletournament_teams.html',
                      {'x': pk, 'tournament': tournament, 'teams': teams})


class SingleTournamentBracket(View):

    def get(self, request, **kwargs):
        pk = self.kwargs['pk']
        tournament = SingleEliminationTournament.objects.get(id=pk)
        teams = tournament.teams.all()
        if tournament.bracket_generated:
            # show the right bracket
            rounds = SingleTournamentRound.objects.all().filter(tournament=tournament)
            return render(request, 'singletournaments/singletournament_bracket.html',
                          {'x': pk, 'tournament': tournament,
                           'teams': teams, 'rounds': rounds})
        else:
            # show some template that its not generated yet
            return render(request, 'singletournaments/no_bracket.html',
                          {'tournament': tournament})
