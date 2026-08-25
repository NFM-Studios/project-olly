from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.generic import View

from matches.models import Match
from profiles.models import UserProfile
from realtime.utils import notify_user
from singletournaments.models import SingleTournamentRuleset
from store.models import deduct_credits
from teams.models import Team

from .forms import DoubleEliminationTournamentJoinPost, DoubleEliminationTournamentLeaveForm
from .models import DoubleEliminationTeam, DoubleEliminationTournament


class List(View):
    def get(self, request):
        tournament_list = DoubleEliminationTournament.objects.filter(active=True).order_by('-start')
        return render(request, 'doubletournaments/doubletournament_list.html',
                      {'tournament_list': tournament_list})


class DoubleEliminationTournamentDetail(View):
    def get(self, request, **kwargs):
        pk = self.kwargs['pk']
        tournament = get_object_or_404(DoubleEliminationTournament, id=pk)
        ruleset = tournament.ruleset
        teams = tournament.teams.all()
        matches = Match.objects.filter(doubleeliminationround__tournament=tournament).distinct()
        user_teams = []
        if not request.user.is_anonymous:
            try:
                profile = UserProfile.objects.get(user=request.user)
                user_teams = list(profile.founder_teams.all()) + list(profile.captain_teams.all())
            except UserProfile.DoesNotExist:
                user_teams = []
        return render(request, 'doubletournaments/doubletournament_detail.html',
                      {'pk': pk, 'tournament': tournament, 'ruleset': ruleset, 'teams': teams,
                       'matches': matches, 'user_teams': user_teams,
                       'winners_rounds': tournament.winners_rounds,
                       'losers_rounds': tournament.losers_rounds})


class DoubleEliminationTournamentJoin(View):
    def get(self, request, pk):
        return redirect('doubletournaments:detail', pk=pk)

    def post(self, request, pk):
        tournament = get_object_or_404(DoubleEliminationTournament, id=pk)
        form = DoubleEliminationTournamentJoinPost(request.POST)
        if not form.is_valid():
            messages.error(request, 'Please select a valid team to join with')
            return redirect('doubletournaments:detail', pk=tournament.pk)
        team = form.cleaned_data['teams']
        try:
            profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            messages.error(request, 'You need a profile to join a tournament')
            return redirect('doubletournaments:detail', pk=tournament.pk)
        if team not in profile.founder_teams.all() and team not in profile.captain_teams.all():
            messages.error(request, "You aren't a captain or founder of this team")
            return redirect('doubletournaments:detail', pk=tournament.pk)

        if tournament.bracket_generated:
            messages.error(request, "The bracket has already been generated for this tournament, new teams aren't "
                                    "permitted")
            return redirect('doubletournaments:detail', pk=tournament.pk)

        now = timezone.now()
        # registration is allowed if an admin has manually opened it
        # (allow_register), or if we are within the registration window
        if not tournament.allow_register:
            if tournament.open_register >= now:
                messages.error(request, 'Registration for this tournament is not open yet')
                return redirect('doubletournaments:detail', pk=tournament.pk)
            if tournament.close_register <= now:
                messages.error(request, 'Registration for this tournament is closed already')
                return redirect('doubletournaments:detail', pk=tournament.pk)

        if tournament.teams.count() >= tournament.size:
            messages.error(request, "This tournament is full")
            return redirect('doubletournaments:detail', pk=tournament.pk)

        if tournament.teams.filter(pk=team.pk).exists():
            messages.error(request, "This team is already in this tournament")
            return redirect('doubletournaments:detail', pk=tournament.pk)

        # roster size check based on the tournament team format
        players = tournament.teamformat + 1
        member_count = team.players.count() + team.captain.count() + (1 if team.founder is not None else 0)
        if member_count <= players:
            messages.error(request, "Your team does not have enough people to play in this tournament")
            return redirect('doubletournaments:detail', pk=tournament.pk)

        # team members may not overlap with teams already registered
        registered_teams = tournament.teams.all()
        for user in list(team.players.all()) + list(team.captain.all()) + ([team.founder] if team.founder else []):
            for otherteam in registered_teams:
                if user in otherteam.players.all() or user in otherteam.captain.all() or user == otherteam.founder:
                    messages.error(request, "There is overlap between users in teams in the tournament")
                    return redirect('doubletournaments:detail', pk=tournament.pk)

        # credits are deducted once from the acting user's profile
        if int(profile.credits) < int(tournament.req_credits):
            messages.error(request, "You do not have enough credits to join this tournament")
            return redirect('doubletournaments:detail', pk=tournament.pk)

        with transaction.atomic():
            tournament.teams.add(team)
            deduct_credits(request.user, tournament.req_credits)
            DoubleEliminationTeam.objects.create(team=team, tournament=tournament)
        notify_user(request.user, title='Joined tournament %s' % tournament.name,
                    description='Your team %s has been registered for %s' % (team.name, tournament.name),
                    sender='Double Elimination', type='general',
                    link='/double-tournaments/%s/' % tournament.pk, pk1=tournament.pk)
        messages.success(request, 'Joined tournament')
        return redirect('doubletournaments:detail', pk=tournament.pk)


class DoubleEliminationTournamentLeave(View):
    def get(self, request, pk):
        return redirect('doubletournaments:detail', pk=pk)

    def post(self, request, pk):
        form = DoubleEliminationTournamentLeaveForm(request.POST)
        tournament = get_object_or_404(DoubleEliminationTournament, id=pk)
        if tournament.bracket_generated:
            messages.error(request, "The bracket has been generated already, you cannot leave the tournament")
            return redirect('doubletournaments:detail', pk=tournament.pk)
        if not form.is_valid():
            messages.error(request, "Invalid form submission")
            return redirect('doubletournaments:detail', pk=tournament.pk)
        if not form.cleaned_data['confirm']:
            messages.error(request, "You submitted without confirming that you wanted to leave")
            return redirect('doubletournaments:detail', pk=tournament.pk)
        user_team = tournament.teams.filter(founder=request.user).first()
        if user_team is None:
            messages.error(request, "You are not in this tournament")
            return redirect('doubletournaments:detail', pk=tournament.pk)
        # note: no credit refund on leaving a double-elimination tournament
        with transaction.atomic():
            DoubleEliminationTeam.objects.filter(tournament=tournament, team=user_team).delete()
            tournament.teams.remove(user_team)
        notify_user(request.user, title='Left tournament %s' % tournament.name,
                    description='Your team %s has been removed from %s' % (user_team.name, tournament.name),
                    sender='Double Elimination', type='general',
                    link='/double-tournaments/%s/' % tournament.pk, pk1=tournament.pk)
        messages.success(request, 'Left tournament %s' % tournament.name)
        return redirect('doubletournaments:detail', pk=tournament.pk)


class DoubleEliminationTournamentTeamsList(View):
    def get(self, request, **kwargs):
        pk = self.kwargs['pk']
        tournament = get_object_or_404(DoubleEliminationTournament, id=pk)
        teams = tournament.teams.all()
        entries = DoubleEliminationTeam.objects.filter(tournament=tournament).select_related('team')
        return render(request, 'doubletournaments/doubletournament_teams.html',
                      {'pk': pk, 'tournament': tournament, 'teams': teams, 'entries': entries})


class DoubleEliminationTournamentBracket(View):
    def get(self, request, **kwargs):
        pk = self.kwargs['pk']
        tournament = get_object_or_404(DoubleEliminationTournament, id=pk)
        teams = tournament.teams.all()
        return render(request, 'doubletournaments/doubletournament_bracket.html',
                      {'pk': pk, 'tournament': tournament, 'teams': teams,
                       'winners_rounds': tournament.winners_rounds,
                       'losers_rounds': tournament.losers_rounds})


class RulesetDetail(View):
    def get(self, request, **kwargs):
        ruleset = get_object_or_404(SingleTournamentRuleset, id=self.kwargs['pk'])
        return render(request, 'doubletournaments/doubletournament_ruleset.html', {'ruleset': ruleset})