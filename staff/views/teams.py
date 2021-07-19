from django.contrib import messages
from django.shortcuts import render, redirect

from staff.forms import *
from teams.models import TeamInvite
from wagers.models import *


def teams_index(request):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        teams_list = Team.objects.all().order_by('id')
        return render(request, 'staff/teams/team_list.html', {'teams_list': teams_list})


def teams_detail(request, pk):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        team = Team.objects.get(id=pk)
        players = team.players.all()
        captains = team.captain.all()

        return render(request, 'staff/teams/team_detail.html',
                      {'team': team, 'players': players, 'captains': captains, 'pk': pk})


def verify_membership(request, pk):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        team = Team.objects.get(id=pk)
        players = team.players.all()
        captains = team.captain.all()
        for x in players:
            userprofile = UserProfile.objects.get(user=x)
            if team not in userprofile.player_teams.all():
                userprofile.player_teams.add(team)
                userprofile.save()

        for y in captains:
            userprofile = UserProfile.objects.get(user=y)
            if team not in userprofile.captain_teams.all():
                userprofile.captain_teams.add(team)
                userprofile.save()

        return redirect('staff:team_detail', pk=pk)


def force_addplayer(request, pk):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        team = Team.objects.get(id=pk)
        if request.method == "GET":
            form = TeamForceAddUser()
            return render(request, 'staff/teams/force_addplayer.html', {'form': form, 'team': team})
        else:
            form = TeamForceAddUser(request.POST)
            if form.is_valid():
                muser = form.cleaned_data['user']
                user = User.objects.get(username=muser)
                try:
                    temp = UserProfile.objects.get(user=user)
                except:
                    messages.error(request, 'Unable to find user')
                    return redirect('staff:team_detail', pk=team.id)
                if (temp.user in team.players.all()) or (temp.user in team.captain.all()) or (temp.user == team.founder):
                    messages.error(request, "This user already exists on the team")
                    return redirect('staff:team_detail', pk=team.id)
                team.players.add(temp.user)
                team.save()
                temp.player_teams.add(team)
                temp.player_teams.save()
                messages.success(request, "Successfully added user to team - as role:player")
                return redirect('staff:team_detail', pk=team.id)
            else:
                messages.error(request, "Unknown Form Error")
                return redirect('staff:team_detail', pk=team.id)


def create_team(request):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        if request.method == 'GET':
            form = CreateTeamForm()
            return render(request, 'staff/teams/team_create.html', {'form': form})
        else:
            form = CreateTeamForm(request.POST)
            if form.is_valid():
                team = form.instance
                team.save()
                messages.success(request, 'Created team')
                return redirect('staff:team_detail', pk=team.id)
            else:
                form = CreateTeamForm(request.POST)
                return render(request, 'staff/teams/team_create.html', {'form': form})


def delete_team(request, pk):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        team = Team.objects.get(id=pk)
        team.players.clear()
        team.delete()
        messages.success(request, 'Team successfully deleted')
        return redirect('staff:teamindex')


def remove_user(request, pk):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        if request.method == 'POST':
            form = RemovePlayerFormPost(request.POST)
            team = Team.objects.get(pk=pk)
            muser = form.data['remove']
            user = User.objects.get(user=muser)
            if user in team.players.all():
                try:
                    team.players.remove(form.data['remove'])
                    team.save()
                except:
                    messages.error(request, "Failed to remove player from team")
                    return redirect('staff:team_detail', pk=team.id)
            elif user in team.captain.all():
                try:
                    team.captain.remove(form.data['remove'])
                    team.save()
                except:
                    messages.error(request, "Failed to remove user as captain from team")
                    return redirect('staff:team_detail', pk=team.id)
            else:
                messages.error(request, "Unable to verify user is on the team as player/captain")
                return redirect('staff:team_detail', pk=team.id)
            messages.success(request, 'Removed user %s from team' % user)
            return redirect('staff:team_detail', pk=pk)
        else:
            form = RemovePlayerForm(request, pk)
            return render(request, 'staff/teams/team_remove_player.html', {'form': form, 'pk': pk})


def getteamrank(request):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        allteams = Team.objects.all()
        if allteams.count() == 0:
            messages.error(request, "There are no teams")
            return redirect('staff:teamindex')
        for i in allteams:
            i.get_rank()
        messages.success(request, "Calculated rank for %s teams" % allteams.count())
        return redirect('staff:teamindex')
