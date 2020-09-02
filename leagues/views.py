from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.shortcuts import redirect
from .models import League, LeagueDivision, LeagueSettings


def list_leagues(request):
    leagues = League.objects.filter(active=True)
    return render(request, 'leagues/leagues_list.html', {'leagues': leagues})


def detail_league(request, pk):
    league = get_object_or_404(League)
    teams = league.teams.all()
    return render(request, 'leagues/league_detail.html', {'league': league, 'teams': teams})


def join_league(request, pk):
    pass


def leave_league(request, pk):
    pass


def detail_league_teams(request, pk):
    league = get_object_or_404(League)
    if league.divisions.count() == 0:
        messages.warning(request, 'There are no divisions for this league yet')
        return redirect('leagues:detail', pk)
    else:
        divisions = league.divisions.all()  # .teams.all()
        teams = []
        for division in divisions:
            teams.append(division.teams.all())
        teams = teams  # .order_by
        return render(request, 'leagues/league_teams.html', {'teams': teams})


def list_league_divisions(request, pk):
    league = get_object_or_404(League)
    if league.divisions.count() == 0:
        messages.warning(request, "There are no divisions for this league yet")
        return redirect('league:detail', pk)
    else:
        divisions = league.divisions.all()

        return render(request, 'leagues/league_divisions.html', {'league': league, 'divisions': divisions})


def detail_league_division(request, pk, divid):
    league = get_object_or_404(League)
    division = LeagueDivision.objects.get(pk=divid)
    matches = division.matches.all()
    return render(request, 'leagues/league_division.html', {'league': league, 'division': division, 'matches': matches})


def detail_league_rules(request, pk):
    pass
