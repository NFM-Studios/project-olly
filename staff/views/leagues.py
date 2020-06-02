from django.contrib import messages
from django.shortcuts import render, redirect
#from django.views.generic import View

#from matches.models import MatchReport, MatchDispute, Match, MapChoice, MapPoolChoice
from staff.forms import *


def create_league(request):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        if request.method == 'GET':
            form = CreateLeagueForm
            return render(request, 'staff/leagues/league_create.html', {'form': form})
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
        return render(request, 'staff/leagues/league_list.html', {'leagues': leagues})


def detail_league(request, pk):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        league = League.objects.get(pk=pk)
        divisions = league.divisions
        return render(request, 'staff/leagues/league_detail.html', {'league': league})


# list all the teams in the league and the divisions
def league_teams(request, pk):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        league = League.objects.get(pk=pk)
        divisions = league.divisions
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
            return render(request, 'staff/leagues/league_edit.html', {'form': form, 'pk':pk, 'league':league})


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
        print(divisions)
        return render(request, 'staff/leagues/league_divisions_list.html', {'league': league, 'divisions': divisions})


def detail_division(request, pk):
    pass


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
                tempdiv = LeagueDivision(name=league.name+" Division "+str(x))
                tempdiv.save()
                ids.append(tempdiv.id)
                league.divisions.add(tempdiv)
                league.save()
            messages.success(request, 'League divisions created with id: '+str(ids))
            return redirect('staff:list_division', pk=league.id)


def league_match_add(request, pk):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied')
    else:
        if request.method == 'POST':
            league = League.objects.get(pk=pk)
            form = AddLeagueMatchForm
            if form.awayteam == '' or form.hometeam == '':
                form.add_error(form, error='Away Team or Home Team values are blank', field=form.awayteam)
                try:
                    awayteam = Team.objects.get(pk=form.awayteam)
                    hometeam = Team.objects.get(pk=form.hometeam)
                except:
                    form.add_error(form, error='Team not found', field=form.awayteam)
                    return redirect('staff:add_match_league')
                try:
                    tempmatch = Match(awayteam=awayteam, hometeam=hometeam, type='league', game=league.game,
                                  platform=league.platform, sport=league.sport, bestof=1, teamformat=league.teamformat)
                    tempmatch.save()
                    division = LeagueDivision.objects.get(pk=form.division)
                    division.matches.add(tempmatch)
                except:
                    messages.error(request, 'Error creating match')
                    return render(request, 'staff/leagues/league_addmatch.html', {'form': form})
        else:
            # its a simple get
            form = AddLeagueMatchForm
            return render(request, 'staff/leagues/league_addmatch.html', {'form': form})


def division_match_list(request, pk, divid):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied')
    else:
        league = League.objects.get(pk=pk)
        division = LeagueDivision.objects.get(pk=pk)
        matches = division.matches
        return render(request, 'staff/leagues/league_matches.html', {'league': league, 'division': division, 'matches':matches })