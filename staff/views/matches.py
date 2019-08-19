from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import View

from matches.models import MatchReport, MatchDispute
from staff.forms import *
from wagers.models import *


def matches_index(request):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        # matches_list = Match.objects.all().order_by('-id')
        tmatches = Match.objects.filter(type__isnull=True)
        wmatches = Match.objects.filter(type='w')
        return render(request, 'staff/matches/matches.html', {'tmatches': tmatches, 'wmatches': wmatches})


def match_detail(request, pk):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        match = Match.objects.get(pk=pk)
        if match.type == "w":
            return render(request, 'staff/wagers/match_wager_detail.html', {'match': match})
        else:
            if match.disputed:
                dispute = MatchDispute.objects.get(match=match)
                return render(request, 'staff/matches/match_detail.html', {'match': match, 'dispute': dispute})
            else:
                return render(request, 'staff/matches/match_detail.html', {'match': match})


def match_edit(request, pk):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        if request.method == 'POST':
            matchobj = Match.objects.get(pk=pk)
            form = EditMatchForm(request.POST, instance=matchobj)
            if form.is_valid():
                form.save()
                messages.success(request, 'Match has been updated')
                return redirect('staff:match_detail', pk=pk)
            else:
                return render(request, 'staff/matches/match_edit.html', {'form': form})
        else:
            matchobj = Match.objects.get(pk=pk)
            form = EditMatchForm(instance=matchobj)
            return render(request, 'staff/matches/match_edit.html', {'form': form, 'pk': pk})


class MatchDeclareWinner(View):
    template_name = 'staff/matches_winner.html'

    def get(self, request, pk):
        user = UserProfile.objects.get(user__username=request.user.username)
        allowed = ['superadmin', 'admin']
        if user.user_type not in allowed:
            return render(request, 'staff/permissiondenied.html')
        else:
            form = DeclareMatchWinnerForm(request, pk)
            return render(request, self.template_name, {'form': form, 'pk': pk})

    def post(self, request, pk):
        user = UserProfile.objects.get(user__username=request.user.username)
        allowed = ['superadmin', 'admin']
        if user.user_type not in allowed:
            return render(request, 'staff/permissiondenied.html')
        else:
            matchobj = Match.objects.get(pk=pk)
            if not matchobj.bye_2 and not matchobj.bye_1:
                form = DeclareMatchWinnerPost(request.POST, instance=matchobj)
                instance = form.instance
                match = Match.objects.get(id=self.kwargs['pk'])
                winner = Team.objects.get(id=form.data['winner'])
                teams = list()
                teams.append(match.hometeam)
                teams.append(match.awayteam)
                teams.remove(winner)
                loser = teams[0]
                instance.match = match
                instance.winner = winner
                instance.loser = loser
                instance.completed = True
                instance.save()
                try:
                    winner.num_matchwin += 1
                    loser.num_matchloss += 1
                    winner.save()
                    loser.save()
                    if match.type == 'w':
                        # the match is a wager
                        wfounder = UserProfile.objects.get(id=winner.founder_id)
                        wmatch = WagerMatch.objects.get(match=match)
                        wfounder.credits += (2 * wmatch.credits)
                        # find a way to log them getting credits
                        for player in winner.players:
                            wplayer = UserProfile.objects.get(user=player)
                            wplayer.total_earning += wmatch.credits
                        messages.success(request, 'Wager Winner declared')
                    messages.success(request, "Winner declared")
                except:
                    messages.error(request, "Match statistics were not properly logged")
                return redirect('staff:matches_index')
            else:
                messages.error(request, 'Bye match, cannot set winner')
                return redirect('staff:matches_index')


def match_delete_winner(request, pk):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        match = Match.objects.get(pk=pk)
        if not match.bye_1 and not match.bye_2:
            match.winner = None
            match.completed = False
            match.reported = False
            match.team1reported = False
            match.team2reported = False
            match.team1reportedwinner = None
            match.team2reportedwinner = None
            match.disputed = False
            match.save()
            for i in MatchReport.objects.filter(match_id=pk):
                i.delete()
            messages.success(request, "Winner reset")
            return redirect('staff:matches_index')
        else:
            messages.error(request, 'Bye match, cannot change winner')
            return redirect('staff:matches_index')


def dispute_detail(request, pk):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        dispute = MatchDispute.objects.get(pk=pk)
        return render(request, 'staff/matches/dispute_detail.html', {'dispute': dispute})


def gamelist(request):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        games = GameChoice.objects.all().order_by('id')
        return render(request, 'staff/matches/game_list.html', {'games': games})


def game_detail(request, pk):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        if request.method == 'POST':
            game = GameChoice.objects.get(pk=pk)
            form = GameChoiceForm(request.POST, request.FILES, instance=game)
            if form.is_valid():
                form.save()
                messages.success(request, 'Game has been updated')
                return redirect('staff:gamelist')
            else:
                return render(request, 'staff/matches/editgame.html', {'form': form})
        else:
            game = GameChoice.objects.get(pk=pk)
            form = GameChoiceForm(instance=game)
            return render(request, 'staff/matches/editgame.html', {'form': form, 'pk': pk})


def delete_game(request, pk):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        game = GameChoice.objects.get(pk=pk)
        game.delete()
        messages.success(request, "Game Deleted")
        return redirect('staff:gamelist')


def create_gamechoice(request):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        if request.method == 'GET':
            form = GameChoiceForm()
            return render(request, 'staff/matches/editgame.html', {'form': form})
        else:
            form = GameChoiceForm(request.POST, request.FILES)
            if form.is_valid():
                gamechoice = form.instance
                gamechoice.save()
                messages.success(request, 'Created Game')
                return redirect('staff:gamelist')
            else:
                form = GameChoiceForm(request.POST, request.FILES)
                return render(request, 'staff/matches/editgame.html', {'form': form})


def platformlist(request):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        platforms = PlatformChoice.objects.all().order_by('id')
        return render(request, 'staff/matches/platform_list.html', {'platforms': platforms})


def platform_detail(request, pk):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        if request.method == 'POST':
            platform = PlatformChoice.objects.get(pk=pk)
            form = PlatformChoiceForm(request.POST, request.FILES, instance=platform)
            if form.is_valid():
                form.save()
                messages.success(request, 'Platform has been updated')
                return redirect('staff:platformlist')
            else:
                return render(request, 'staff/matches/editplatform.html', {'form': form})
        else:
            platform = PlatformChoice.objects.get(pk=pk)
            form = PlatformChoiceForm(instance=platform)
            return render(request, 'staff/matches/editplatform.html', {'form': form, 'pk': pk})


def delete_platform(request, pk):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        platform = PlatformChoice.objects.get(pk=pk)
        platform.delete()
        messages.success(request, "Platform Deleted")
        return redirect('staff:platformlist')


def create_platformchoice(request):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        if request.method == 'GET':
            form = PlatformChoiceForm()
            return render(request, 'staff/matches/editplatform.html', {'form': form})
        else:
            form = PlatformChoiceForm(request.POST, request.FILES)
            if form.is_valid():
                platformchoice = form.instance
                platformchoice.save()
                messages.success(request, 'Created Game')
                return redirect('staff:platformlist')
            else:
                form = GameChoiceForm(request.POST, request.FILES)
                return render(request, 'staff/matches/editplatform.html', {'form': form})


def map_list(request):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        maps = MapChoice.objects.all().order_by('id')
        return render(request, 'staff/matches/map_list.html', {'maps': maps})


def map_detail(request, pk):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        if request.method == 'POST':
            mapchoice = MapChoice.objects.get(pk=pk)
            form = MapChoiceForm(request.POST, request.FILES, instance=mapchoice)
            if form.is_valid():
                form.save()
                messages.success(request, 'Map has been updated')
                return redirect('staff:maplist')
            else:
                return render(request, 'staff/matches/editmap.html', {'form': form})
        else:
            mapchoice = MapChoice.objects.get(pk=pk)
            form = MapChoiceForm(instance=mapchoice)
            return render(request, 'staff/matches/editmap.html', {'form': form, 'pk': pk})


def delete_map(request, pk):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        mapchoice = MapChoice.objects.get(pk=pk)
        mapchoice.delete()
        messages.success(request, "Map Deleted")
        return redirect('staff:map_list')


def create_mapchoice(request):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        if request.method == 'GET':
            form = MapChoiceForm()
            return render(request, 'staff/matches/editmap.html', {'form': form})
        else:
            form = MapChoiceForm(request.POST, request.FILES)
            if form.is_valid():
                mapchoice = form.instance
                mapchoice.save()
                messages.success(request, 'Created Map')
                return redirect('staff:map_list')
            else:
                form = GameChoiceForm(request.POST, request.FILES)
                return render(request, 'staff/matches/editmap.html', {'form': form})


def map_pool_list(request):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        mappools = MapPoolChoice.objects.all().order_by('id')
        return render(request, 'staff/matches/map_pool_list.html', {'mappools': mappools})


def map_pool_detail(request, pk):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        if request.method == 'POST':
            mappoolchoice = MapPoolChoice.objects.get(pk=pk)
            form = MapPoolChoiceForm(request.POST, request.FILES, instance=mappoolchoice)
            if form.is_valid():
                form.save()
                messages.success(request, 'Map pool has been updated')
                return redirect('staff:map_pool_list')
            else:
                return render(request, 'staff/matches/editmappool.html', {'form': form})
        else:
            mappoolchoice = MapPoolChoice.objects.get(pk=pk)
            form = MapPoolChoiceForm(instance=mappoolchoice)
            return render(request, 'staff/matches/editmappool.html', {'form': form, 'pk': pk})


def delete_map_pool(request, pk):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        mappoolchoice = MapPoolChoice.objects.get(pk=pk)
        mappoolchoice.delete()
        messages.success(request, "Map Pool Deleted")
        return redirect('staff:map_pool_list')


def create_map_pool_choice(request):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        if request.method == 'GET':
            form = MapPoolChoiceForm()
            return render(request, 'staff/matches/editmappool.html', {'form': form})
        else:
            form = MapPoolChoiceForm(request.POST, request.FILES)
            if form.is_valid():
                mappoolchoice = form.instance
                mappoolchoice.save()
                messages.success(request, 'Created Map Pool')
                return redirect('staff:map_pool_list')
            else:
                form = GameChoiceForm(request.POST, request.FILES)
                return render(request, 'staff/matches/editmappool.html', {'form': form})
