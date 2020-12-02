from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.shortcuts import redirect
from .models import League, LeagueDivision, LeagueSettings
from profiles.models import User, UserProfile

def list_leagues(request):
    leagues = League.objects.filter(active=True)
    return render(request, 'leagues/leagues_list.html', {'leagues': leagues})


def detail_league(request, pk):
    league = get_object_or_404(League, pk=pk)
    teams = league.teams.all()
    if len(league.divisions) == 1:
        # there is only one division show the matches in the one page
        division = league.divisions.first()
        matches = division.matches
        return render(request, 'leagues/league_division.html',
                      {'league': league, 'matches': matches, 'division': division})
    return render(request, 'leagues/league_detail.html', {'league': league, 'teams': teams})


def join_league(request, pk):
    league = get_object_or_404(League, pk=pk)
    # TODO - create join league form and send to template
    userprofile = UserProfile.objects.get(user__username=request.user.username)
    # TODO - create join league form and send to template
    if request.method == 'GET':
        # send the form
        pass
    elif request.method == 'POST':
        # try and get them to join the league
        # make sure enough players exist on the team
        if league.req_credits > 0:
            # there is a credit fee, check the user has enough credits
            if userprofile.credits >= league.req_credits:
                # they do have enough credits
                userprofile.credits = userprofile.credits - league.req_credits
                userprofile.save()
            else:
                messages.error(request, "You do not have enough credits to enter your team in this league")
                return redirect('leagues:detail', pk=pk)
        # now lets check that the team has enough players


    return render(request, 'leagues/league_join.html', {'league': league})


def leave_league(request, pk):
    # find out which team wants to leave
    pass


def detail_league_teams(request, pk):
    pass


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
    pass
