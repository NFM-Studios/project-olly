from django.shortcuts import render, get_object_or_404
from .models import League, LeagueDivision, LeagueSettings


def list_leagues(request):
    leagues = League.objects.filter(active=True)
    return render(request, 'leagues/leagues_list.html', {'leagues': leagues})


def detail_league(request, pk):
    league = get_object_or_404(League, pk)
    return render(request, 'leagues/league_detail.html', {'league': league})


def join_league(request, pk):
    pass


def detail_league_teams(request, pk):
    pass


def detail_league_divisions(request, pk):
    pass


def detail_league_rules(request, pk):
    pass