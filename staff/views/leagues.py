from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
import datetime
# from django.views.generic import View

# from matches.models import MatchReport, MatchDispute, Match, MapChoice, MapPoolChoice
from staff.forms import *


def create_league(request):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        if request.method == 'GET':
            form = CreateLeagueForm
            time = datetime.datetime.utcnow()
            return render(request, 'staff/leagues/league_create.html', {'form': form, 'time': time})
        else:
            # the form is posting, lets start validating
            form = CreateLeagueForm(request.POST, request.FILES)
            if form.is_valid():
                league = form.instance
                league.save()
                messages.success(request, 'Created League')
                return redirect('staff:list_league')
            else:
                form = CreateLeagueForm(request.POST)
                return render(request, 'staff/leagues/league_create.html', {'form': form})


def list_league(request):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        leagues = League.objects.all()
        time = datetime.datetime.utcnow()
        return render(request, 'staff/leagues/league_list.html', {'leagues': leagues, 'time': time})


def detail_league(request, pk):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        league = League.objects.get(pk=pk)
        divisions = league.divisions.all()
        time = datetime.datetime.utcnow()
        return render(request, 'staff/leagues/league_detail.html',
                      {'league': league, 'divisions': divisions, 'time': time})


# list all the teams in the league and the divisions
def league_teams(request, pk):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        league = League.objects.get(pk=pk)
        divisions = league.divisions.all()
        return render(request, 'staff/leagues/league_teams.html', {'league': league, 'divisions': divisions})


# used for adding teams to a league before the league is launched
def league_teams_add(request, pk):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.hmtl')
    else:
        league = League.objects.get(pk=pk)
        return render(request, 'staff/leagues/league_teams_add.html', {'league': league})


def edit_league(request, pk):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        if request.method == 'POST':
            league = League.objects.get(pk=pk)
            form = CreateLeagueForm(request.POST, request.FILES, instance=league)
            if form.is_valid():
                form.save()
                messages.success(request, 'League has been updated')
                return redirect('staff:list_league')
            else:
                messages.error(request, 'Form validation error')
                return redirect('staff:list_league')
        else:
            league = League.objects.get(pk=pk)
            form = CreateLeagueForm(instance=league)
            time = datetime.datetime.utcnow()
            return render(request, 'staff/leagues/league_edit.html',
                          {'form': form, 'pk': pk, 'league': league, 'time': time})


def list_league_settings(request):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        settings = LeagueSettings.objects.all()
        return render(request, 'staff/leagues/league_settings_list.html', {'settings': settings})


def create_league_settings(request):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        if request.method == 'GET':
            form = CreateLeagueSettingsForm
            return render(request, 'staff/leagues/league_settings_create.html', {'form': form})
        else:
            form = CreateLeagueSettingsForm(request.POST)
            if form.is_valid():
                settings = form.instance
                settings.save()
                messages.success(request, 'Created League Settings')
                return redirect('staff:list_league_settings')
            else:
                messages.error(request, 'A form validation error has occured')
                form = CreateLeagueSettingsForm(request.POST)
                return render(request, 'staff/leagues/league_settings_create.html', {'form': form})


def edit_league_settings(request, pk):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        if request.method == 'POST':
            league = LeagueSettings.objects.get(pk=pk)
            form = EditLeagueSettingsForm(request.POST, request.FILES, instance=league)
            if form.is_valid():
                form.save()
                messages.success(request, 'League Settings has been updated')
                return redirect('staff:list_league_settings')
            else:
                return render(request, 'staff/leagues/league_settings_edit.html', {'form': form})
        else:
            league = LeagueSettings.objects.get(pk=pk)
            form = EditLeagueSettingsForm(instance=league)
            return render(request, 'staff/leagues/league_settings_edit.html', {'form': form, 'pk': pk})


def detail_league_settings(request, pk):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        settings = LeagueSettings.objects.get(pk=pk)
        return render(request, 'staff/leagues/league_settings_detail.html', {'settings': settings})


def launch_league(request, pk):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        league = League.objects.get(pk=pk)
        settings = league.settings


def list_division(request, pk):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        league = League.objects.get(pk=pk)
        divisions = league.divisions.all()
        return render(request, 'staff/leagues/league_divisions_list.html', {'league': league, 'divisions': divisions})


def detail_division(request, pk, divid):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        league = League.objects.get(pk=pk)
        division = LeagueDivision.objects.get(pk=divid)
        matches = division.matches.all()
        return render(request, 'staff/leagues/league_division_detail.html',
                      {'league': league, 'division': division, 'matches': matches})
    # show add match, add team button


def add_division(request, pk):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        league = League.objects.get(pk=pk)
        tempdiv = LeagueDivision()
        tempdiv.save()
        tempdiv.name = league.name + " Division " + str(tempdiv.pk)
        league.divisions.add(tempdiv)
        messages.success(request, "Division manually added")
        return redirect('staff:detail_league', pk=pk)


def create_divisions(request, pk):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        league = League.objects.get(pk=pk)
        if league.divisions.count() >= league.settings.num_divisions:
            messages.error(request, 'ERROR: There are already too many divisions created')
            return redirect('staff:list_division', pk=league.id)
        else:
            # lets make the divisions
            ids = []
            for x in range(league.settings.num_divisions):
                tempdiv = LeagueDivision()
                tempdiv.save()
                tempdiv.name = league.name + " Division " + str(tempdiv.pk)
                tempdiv.save()
                ids.append(tempdiv.pk)
                league.divisions.add(tempdiv)
                league.save()
            messages.success(request, 'League divisions created with id: ' + str(ids))
            return redirect('staff:list_division', pk=league.id)


def division_match_add(request, pk, divid):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied')
    else:
        league = League.objects.get(pk=pk)
        division = LeagueDivision.objects.get(pk=divid)
        if request.method == 'POST':
            form = AddLeagueMatchForm(request.POST)
            if form.is_valid():
                try:
                    away = False
                    home = False
                    awayteam = Team.objects.get(pk=form.cleaned_data['awayteam'])
                    hometeam = Team.objects.get(pk=form.cleaned_data['hometeam'])
                    for team in division.teams.all():
                        if team.team.pk is awayteam.pk:
                            away = True
                        if team.team.pk is hometeam.pk:
                            home = True
                    if away and home:
                        tempmatch = Match(awayteam=awayteam, hometeam=hometeam, type='league', game=league.game,
                                          platform=league.platform, sport=league.sport, bestof=1,
                                          teamformat=league.teamformat, conference_match=False, map_pool=league.maps)
                        tempmatch.save()
                    else:
                        messages.error(request,
                                       "One of the teams is not in the division, adding as non-conference match")
                        nonconf = Match(awayteam=awayteam, hometeam=hometeam, type='league', game=league.game,
                                        platform=league.platform, sport=league.sport, bestof=1,
                                        teamformat=league.teamformat, conference_match=True, map_pool=league.maps)
                        nonconf.save()
                        league.non_conference.add(nonconf)
                        league.save()
                        messages.success(request, "Successfully added match to league")
                        messages.success(request, "Successfully added as non-conference match")
                        return redirect('staff:detail_division', pk=league.id, divid=division.pk)
                    division = LeagueDivision.objects.get(pk=division.pk)
                    division.matches.add(tempmatch)
                    return redirect('staff:detail_division', pk=league.id, divid=division.id)
                except ObjectDoesNotExist:
                    form.add_error(form, error='Team not found', field=form.awayteam)
                    return redirect('staff:add_match_league')
        else:
            # its a simple get
            form = AddLeagueMatchForm()
            return render(request, 'staff/leagues/league_addmatch.html',
                          {'form': form, 'league': league, 'division': division})


def division_add_team(request, pk, divid):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        league = League.objects.get(pk=pk)
        division = LeagueDivision.objects.get(pk=divid)
        if request.method == 'POST':
            form = DivisionAddTeamForm(request.POST)
            if form.is_valid():
                try:
                    team = Team.objects.get(pk=form.cleaned_data['teamid'])
                except ObjectDoesNotExist:
                    messages.error(request, 'Team does not exist')
                    return redirect('staff:detail_division', pk=league.pk, divid=division.pk)
                if team in division.teams.all():
                    messages.error(request, 'That Team already exists in the division')
                    return redirect('staff:detail_division', pk=league.pk, divid=division.pk)
                temp = LeagueTeam(team=team)
                temp.save()
                division.teams.add(temp)
                division.save()
                messages.success(request, 'Team has been added to the division')
                return redirect('staff:detail_division', pk=league.pk, divid=division.pk)
            else:
                messages.error(request, 'Form validation error')
                return redirect('staff:detail_division', pk=league.pk, divid=division.pk)
        else:
            form = DivisionAddTeamForm()
            return render(request, 'staff/leagues/league_division_addteam.html',
                          {'division': division, 'league': league, 'form': form})


def division_match_list(request, pk, divid):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        league = League.objects.get(pk=pk)
        division = LeagueDivision.objects.get(pk=divid)
        matches = division.matches.all()
        return render(request, 'staff/leagues/league_division_matches.html',
                      {'league': league, 'division': division, 'matches': matches})


def bulk_match_create(request, pk, divid=0):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied')
    else:
        league = League.objects.get(pk=pk)
