from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from profiles.models import Notification, UserProfile

from .forms import LeagueJoinForm, LeagueLeaveForm
from .models import League, LeagueDivision, LeagueTeam

# minimum roster size required for each team format (index = teamformat value)
TEAMFORMAT_MIN_PLAYERS = {0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6}


def list_leagues(request):
    leagues = League.objects.filter(active=True)
    return render(request, 'leagues/leagues_list.html', {'leagues': leagues})


def detail_league(request, pk):
    league = get_object_or_404(League, pk=pk)
    teams = league.teams.all()
    if not league.divisions.exists():
        # there are no divisions
        return render(request, 'leagues/league_detail.html',
                      {'league': league, 'teams': teams, 'division': 0})

    else:
        standings = LeagueTeam.objects.none()
        division = league.divisions.all()
        return render(request, 'leagues/league_detail.html',
                      {'league': league, 'division': division, 'standings': standings, 'teams': teams})


def _pick_division(league):
    """Return the LeagueDivision a new team should be placed into.

    Teams are balanced across the league's existing divisions, never exceeding
    the max division size from the league settings. If every division is full
    (or none exist yet) a new division is created.
    """
    max_size = league.settings.max_division_size
    open_divisions = [d for d in league.divisions.all() if d.teams.count() < max_size]
    if open_divisions:
        return min(open_divisions, key=lambda d: d.teams.count())
    division = LeagueDivision.objects.create()
    league.divisions.add(division)
    return division


def join_league(request, pk):
    league = get_object_or_404(League, pk=pk)
    userprofile = get_object_or_404(UserProfile, user=request.user)

    if request.method != 'POST':
        return redirect('leagues:detail', pk=pk)

    form = LeagueJoinForm(request.POST, user=request.user)
    if not form.is_valid():
        messages.error(request, "Please select a valid team to join with")
        return redirect('leagues:detail', pk=pk)
    team = form.cleaned_data['team']

    if request.user != team.founder and request.user not in team.captain.all():
        messages.error(request, "You aren't the founder or a captain of this team")
        return redirect('leagues:detail', pk=pk)

    now = timezone.now()
    if not league.allow_register:
        if league.open_register >= now:
            messages.error(request, 'Registration for this league is not open yet')
            return redirect('leagues:detail', pk=pk)
        if league.close_register <= now:
            messages.error(request, 'Registration for this league is closed already')
            return redirect('leagues:detail', pk=pk)

    if league.teams.count() >= league.size:
        messages.error(request, "This league is full")
        return redirect('leagues:detail', pk=pk)

    if league.teams.filter(team=team).exists():
        messages.error(request, "Your team is already in this league")
        return redirect('leagues:detail', pk=pk)

    min_players = TEAMFORMAT_MIN_PLAYERS.get(league.teamformat)
    member_count = team.players.count() + team.captain.count() + (1 if team.founder is not None else 0)
    if min_players is not None and member_count < min_players:
        messages.error(request, "Your team does not have enough players for this league's team format")
        return redirect('leagues:detail', pk=pk)

    with transaction.atomic():
        if league.req_credits > 0:
            if userprofile.credits < league.req_credits:
                messages.error(request, "You do not have enough credits to enter your team in this league")
                return redirect('leagues:detail', pk=pk)
            userprofile.credits = userprofile.credits - league.req_credits
            userprofile.save()

        league_team, _ = LeagueTeam.objects.get_or_create(team=team)
        league.teams.add(league_team)
        division = _pick_division(league)
        division.teams.add(league_team)

        notification = Notification(type='league', title="Your team has joined a league",
                                    description="%s has been entered into %s" % (team.name, league.name),
                                    link='leagues:detail', pk1=league.pk)
        notification.save()
        userprofile.notifications.add(notification)

    messages.success(request, "Your team has been entered into the league")
    return redirect('leagues:detail', pk=pk)


def leave_league(request, pk):
    league = get_object_or_404(League, pk=pk)

    if request.method != 'POST':
        return redirect('leagues:detail', pk=pk)

    form = LeagueLeaveForm(request.POST, user=request.user)
    if not form.is_valid():
        messages.error(request, "Please select a valid team to leave with")
        return redirect('leagues:detail', pk=pk)
    team = form.cleaned_data['team']

    if request.user != team.founder and request.user not in team.captain.all():
        messages.error(request, "You aren't the founder or a captain of this team")
        return redirect('leagues:detail', pk=pk)

    with transaction.atomic():
        league_team = league.teams.filter(team=team).first()
        if league_team is None:
            messages.error(request, "Your team is not in this league")
            return redirect('leagues:detail', pk=pk)
        # deleting the LeagueTeam record removes it from league.teams and from
        # every division it was placed into. no refund is given on leaving.
        league_team.delete()

        userprofile = UserProfile.objects.get(user=request.user)
        notification = Notification(type='league', title="Your team has left a league",
                                    description="%s has been removed from %s" % (team.name, league.name),
                                    link='leagues:detail', pk1=league.pk)
        notification.save()
        userprofile.notifications.add(notification)

    messages.success(request, "Your team has left the league")
    return redirect('leagues:detail', pk=pk)


def detail_league_teams(request, pk):
    # show all the teams in the league
    # get all divisions first
    league = League.objects.get(pk=pk)
    if league.divisions.count() == 0:
        messages.error(request, "There are no divisions or teams in this league yet, check back later")
        return redirect('league:list')
    teams = []
    for x in league.divisions.all():
        for y in x.teams.all():
            teams.append(y)

    return render(request, "leagues/league_teams.html", {'teams': teams, 'league': league})


def list_league_divisions(request, pk):
    league = get_object_or_404(League, pk=pk)
    if league.divisions.count() == 0:
        messages.warning(request, "There are no divisions for this league yet")
        return redirect('league:detail', pk)
    else:
        divisions = league.divisions.all()

        return render(request, 'leagues/league_divisions.html', {'league': league, 'divisions': divisions})


def detail_league_division(request, pk, divid):
    league = get_object_or_404(League, pk=pk)
    division = LeagueDivision.objects.get(pk=divid)
    matches = division.matches.all()
    teams = division.teams.all().order_by('-points')
    return render(request, 'leagues/league_division.html', {'league': league, 'division': division, 'matches': matches,
                                                            'teams': teams})


def detail_league_rules(request, pk):
    league = get_object_or_404(League, pk=pk)
    rules = league.ruleset
    return render(request, 'singletournaments/ruleset_detail.html', {'ruleset': rules})