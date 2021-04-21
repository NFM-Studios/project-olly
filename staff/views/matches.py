from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import View
from matches.models import *
from django.template.loader import render_to_string
from django.conf import settings
from staff.forms import *
from wagers.models import *
from profiles.models import UserProfile, Notification
from django.core.mail import EmailMessage
import datetime
from django.contrib.sites.shortcuts import get_current_site


def matches_index(request):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        # matches_list = Match.objects.all().order_by('-id')
        tmatches = Match.objects.filter(type="singletournament")
        wmatches = Match.objects.filter(type='w')
        lmatches = Match.objects.filter(type="league")
        return render(request, 'staff/matches/matches.html',
                      {'tmatches': tmatches, 'wmatches': wmatches, 'lmatches': lmatches})


def disputed_matches(request):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        # matches_list = Match.objects.all().order_by('-id')
        tmatches = Match.objects.filter(type__isnull=True, disputed=True)
        wmatches = Match.objects.filter(type='w', disputed=True)
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
        time = datetime.datetime.utcnow()
        if request.method == 'POST':
            matchobj = Match.objects.get(pk=pk)
            form = EditMatchForm(request.POST, instance=matchobj)
            if form.is_valid():
                form.save()
                messages.success(request, 'Match has been updated')
                for x in matchobj.awayteam.players.all():
                    temp = Notification(title="Match has been updated", type=1,
                                        description="One of your teams matches has been updated!",
                                        link="matches:detail", pk1=matchobj.pk, datetime=datetime.datetime.utcnow())
                    tp = UserProfile.objects.get(user=x)
                    temp.save()
                    tp.notifications.add(temp)
                    tp.save()
                for y in matchobj.hometeam.players.all():
                    temp = Notification(title="Match has been updated", type=1,
                                        description="One of your teams matches has been updated!",
                                        link="matches:detail", pk1=matchobj.pk, datetime=datetime.datetime.utcnow())
                    tp = UserProfile.objects.get(user=y)
                    temp.save()
                    tp.notifications.add(temp)
                    tp.save()
                for x in matchobj.awayteam.captain.all():
                    temp = Notification(title="Match has been updated", type=1,
                                        description="One of your teams matches has been updated!",
                                        link="matches:detail", pk1=matchobj.pk, datetime=datetime.datetime.utcnow())
                    tp = UserProfile.objects.get(user=x)
                    temp.save()
                    tp.notifications.add(temp)
                    tp.save()
                for y in matchobj.hometeam.players.all():
                    temp = Notification(title="Match has been updated", type=1,
                                        description="One of your teams matches has been updated!",
                                        link="matches:detail", pk1=matchobj.pk, datetime=datetime.datetime.utcnow())
                    tp = UserProfile.objects.get(user=y)
                    temp.save()
                    tp.notifications.add(temp)
                    tp.save()
                messages.success(request, "Notification sent successfully to both teams")
                return redirect('staff:match_detail', pk=pk)
            else:
                return render(request, 'staff/matches/match_edit.html', {'form': form, 'time': time, 'pk': pk})
        else:
            matchobj = Match.objects.get(pk=pk)
            form = EditMatchForm(instance=matchobj)
            return render(request, 'staff/matches/match_edit.html', {'form': form, 'pk': pk, 'time': time})


class MatchDeclareWinner(View):
    template_name = 'staff/matches/matches_winner.html'

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
            if matchobj.type == "league":
                form = DeclareMatchWinnerPost(request.POST, instance=matchobj)
                instance = form.instance
                match = Match.objects.get(id=self.kwargs['pk'])
                winner = Team.objects.get(id=form.data['winner'])
                league = None
                division = None
                for x in League.objects.all():
                    for y in LeagueDivision.objects.all():
                        if match in y.matches:
                            league = x
                            division = y
                            messages.success(request, "Found match league and division")
                if league is None or division is None:
                    messages.error(request, "Failed to find league or division this match is apart of")
                    return redirect('staff:match_detail', pk=match.pk)
                # leagueteam = division.teams.all()
                awayleagueteam = None
                homeleagueteam = None
                for z in division.teams.all():
                    if z.team == match.awayteam:
                        # found away team
                        awayleagueteam = z
                    if z.team == match.hometeam:
                        homeleagueteam = z
                if awayleagueteam is None or homeleagueteam is None:
                    messages.error(request, "Unable to find home or away league team objects")
                    return redirect('staff:match_detail', pk=match.pk)
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
                if loser == match.awayteam:
                    awayleagueteam.losses += 1
                    awayleagueteam.save()
                    match.awayteam.num_losses += 1
                    match.hometeam.num_wins += 1
                    homeleagueteam.wins += 1
                    homeleagueteam.save()
                elif loser == match.hometeam:
                    awayleagueteam.wins += 1
                    homeleagueteam.losses += 1
                    awayleagueteam.save()
                    homeleagueteam.save()
                    match.awayteam.num_wins += 1
                    match.hometeam.num_losses += 1

                # TODO: 107
                pass
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
                    for player in winner.players | winner.captain:
                        tp = UserProfile.objects.get(user=player)
                        notif = Notification(title="You won a match!", type=1,
                                             description="A match your team was in was finalized and your team won!" +
                                                         " Time to celebrate!", link="matches:detail", pk1=match.pk, datetime=datetime.datetime.utcnow())
                        notif.save()
                        tp.notifications.add(notif)
                        tp.save()
                        messages.success(request, "Winning team players and captains notified about the victory")
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
        if match.type == "league":
            # TODO: #107
            pass
        else:
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


def delete_sport(request, pk):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        sport = SportChoice.objects.get(pk=pk)
        sport.delete()
        messages.success(request, "Sport Deleted")
        return redirect('staff:sportlist')


def create_sportchoice(request):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        if request.method == 'GET':
            form = PlatformChoiceForm()
            return render(request, 'staff/matches/editplatform.html', {'form': form})
        else:
            form = SportChoiceForm(request.POST)
            if form.is_valid():
                sportchoice = form.instance
                sportchoice.save()
                messages.success(request, 'Created Sport')
                return redirect('staff:platformlist')
            else:
                form = SportChoiceForm(request.POST)
                return render(request, 'staff/matches/editplatform.html', {'form': form})


def sport_detail(request, pk):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        if request.method == 'POST':
            sport = SportChoice.objects.get(pk=pk)
            form = SportChoiceForm(request.POST, instance=sport)
            if form.is_valid():
                form.save()
                messages.success(request, 'Sport has been updated')
                return redirect('staff:sportlist')
            else:
                return render(request, 'staff/matches/editsport.html', {'form': form})
        else:
            platform = PlatformChoice.objects.get(pk=pk)
            form = PlatformChoiceForm(instance=platform)
            return render(request, 'staff/matches/editsport.html', {'form': form, 'pk': pk})


def sportlist(request):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        sports = SportChoice.objects.all().order_by('id')
        return render(request, 'staff/matches/sport_list.html', {'sports': sports})


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


def pick_map(request, pk):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        match = Match.objects.get(pk=pk)
        match.maps.clear()
        match.save()
        if match.bestof == 1:
            # bo1
            # make sure the mappoolchoice is big enough
            pool = match.map_pool.maps
            if pool.count() >= 1:
                chosen_map = pool.all().order_by("?").first()
                match.maps.add(chosen_map)
                match.save()
                messages.success(request, "Maps updated!")
                return redirect('staff:match_detail', pk=pk)
            else:
                messages.error(request, "There are not enough maps in this map pool for Best of 1")
                return redirect('staff:match_detail', pk=pk)
        elif match.bestof == 2:
            # bo2
            pool = match.map_pool.maps
            if pool.count() >= 2:
                chosen_map = pool.all().order_by("?").first()
                match.maps.add(chosen_map)
                match.save()
                pool.remove(chosen_map)
                # pool.save()
                chosen_map2 = pool.all().order_by("?").first()
                match.maps.add(chosen_map2)
                match.save()
                messages.success(request, "Maps updated!")
                return redirect('staff:match_detail', pk=pk)
            else:
                messages.error(request, "There are not enough maps in this map pool for Best of 2")
                return redirect('staff:match_detail', pk=pk)

        elif match.bestof == 3:
            # bo3
            # make sure the mappoolchoice is big enough
            pool = match.map_pool.maps
            if pool.count() >= 3:
                chosen_map = pool.all().order_by("?").first()
                pool.remove(chosen_map)
                # pool.save()
                match.maps.add(chosen_map)
                match.save()
                chosen_map2 = pool.all().order_by("?").first()
                pool.remove(chosen_map2)
                # pool.save()
                match.maps.add(chosen_map2)
                match.save()
                chosen_map3 = pool.all().order_by("?").first()
                pool.remove(chosen_map3)
                # pool.save()
                match.maps.add(chosen_map3)
                match.save()
                match.maps.add(chosen_map3)
                match.save()
                messages.success(request, "Maps updated!")
                return redirect('staff:match_detail', pk=pk)
            else:
                messages.error(request, "There are not enough maps in this map pool for Best of 3")
                return redirect('staff:match_detail', pk=pk)

        elif match.bestof == 4:
            # bo4
            # make sure the mappoolchoice is big enough
            pool = match.map_pool.maps
            if pool.count() >= 4:
                chosen_map = pool.all().order_by("?").first()
                pool.remove(chosen_map)
                # pool.save()
                match.maps.add(chosen_map)
                match.save()
                chosen_map2 = pool.all().order_by("?").first()
                pool.remove(chosen_map2)
                # pool.save()
                match.maps.add(chosen_map2)
                match.save()
                chosen_map3 = pool.all().order_by("?").first()
                pool.remove(chosen_map3)
                # pool.save()
                match.maps.add(chosen_map3)
                match.save()
                chosen_map4 = pool.all().order_by("?").first()
                pool.remove(chosen_map4)
                # pool.save()
                match.maps.add(chosen_map4)
                match.save()
                messages.success(request, "Maps updated!")
                return redirect('staff:match_detail', pk=pk)
            else:
                messages.error(request, "There are not enough maps in this map pool for Best of 4")
                return redirect('staff:match_detail', pk=pk)

        elif match.bestof == 5:
            # bo5
            # make sure the mappoolchoice is big enough
            pool = match.map_pool.maps
            if pool.count() >= 5:
                chosen_map = pool.all().order_by("?").first()
                pool.remove(chosen_map)
                # pool.save()
                chosen_map2 = pool.all().order_by("?").first()
                pool.remove(chosen_map2)
                # pool.save()
                chosen_map3 = pool.all().order_by("?").first()
                pool.remove(chosen_map3)
                # pool.save()
                chosen_map4 = pool.all().order_by("?").first()
                pool.remove(chosen_map4)
                # pool.save()
                chosen_map5 = pool.all().order_by("?").first()
                pool.remove(chosen_map5)
                # pool.save()
                match.maps.add(chosen_map)
                match.maps.add(chosen_map2)
                match.maps.add(chosen_map3)
                match.maps.add(chosen_map4)
                match.maps.add(chosen_map5)
                match.save()
                messages.success(request, "Maps updated!")
                return redirect('staff:match_detail', pk=pk)
            else:
                messages.error(request, "There are not enough maps in this map pool for Best of 5")
                return redirect('staff:match_detail', pk=pk)

        else:
            messages.error(request, 'Unknown BestOf selected for this match')
            return redirect('staff:match_detail', pk=pk)

        """
    (1, 'Best of 1'),
    (2, 'Best of 2'),
    (3, 'Best of 3'),
    (4, 'Best of 4'),
    (5, 'Best of 5'),
    """


def match_checkins(request, pk):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        mymatch = Match.objects.get(pk=pk)
        checkins = MatchCheckIn.objects.filter(match=mymatch)
        return render(request, 'staff/matches/checkins.html', {'checkins': checkins, 'mymatch': mymatch})


def delete_checkin(request, pk, checkinid):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        checkin = MatchCheckIn.objects.get(pk=pk)
        checkin.delete()
        checkin.save()
        messages.success(request, "Checkin #" + checkin.pk + " has been deleted")
        return redirect('staff:index')


def match_stats_create(request, pk):
    pass


def set_dispute_match(request, pk):
    # set the specific match as disputed

    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        match = Match.objects.get(pk=pk)
        stats = MatchStats()
        team1 = match.awayteam
        team2 = match.hometeam
        # match.disputed = True
        for i in [match.team1.players, match.team2.players]:
            temp = Notification(title="A match you're playing in is disputed!", description="Captains, please visit "
                                                                                            "the match page for more"
                                                                                            "details on resolving this",
                                sender="Match Manager", type='match', link='match:detail', pk1=match.pk, datetime=datetime.datetime.utcnow())
            temp.datetime = datetime.datetime.now()
            temp.save()
            userprofile = UserProfile.objects.get(user=i.user)
            userprofile.notifications.add(temp)
            userprofile.save()
            if i.user.email_enabled:
                current_site = get_current_site(request)
                mail_subject = settings.SITE_NAME + ' match disputed!'
                message = render_to_string('matches/dispute_email.html', {
                    'user': i.username,
                    'site': settings.SITE_NAME,
                    'domain': current_site.domain,
                    'pk': match.pk
                })
                to_email = i.email
                email = EmailMessage(
                    mail_subject, message, from_email=settings.FROM_EMAIL, to=[to_email]
                )
                email.send()

        dispute = MatchDispute(id=match.id, match=match, team1=match.team1, team2=match.team2)
        dispute.save()
        messages.success(request, "Set the match as disputed, notified users, and created the Match Dispute")
        return redirect('staff:match_detail', pk=match.id)


def create_match_config(request, pk):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        # create the get5 config for the match
        match = Match.objects.get(pk=pk)
        if match.config_generated:
            messages.error(request, "A config has already been generated for this match")
            return redirect('staff:match_detail', pk=match.pk)
        if match.awayteam.tag is None:
            messages.error(request, "Away Team has no Team Tag set! Have the captain/founder add a team tag on the"
                                    " edit team page")
            return redirect('staff:match_detail', pk=match.pk)
        elif match.hometeam.tag is None:
            messages.error(request, "Home Team has no Team Tag set! Have the captain/founder add a team tag on the"
                                    " edit team page")
            return redirect('staff:match_detail', pk=match.pk)
        data = {}
        data['matchid'] = match.pk
        data['num_maps'] = 1
        data['players_per_team'] = 5
        data['min_players_to_ready'] = 5
        data['min_spectators_to_ready'] = 0
        data['skip_veto'] = False
        # TEAM2 IS HOME
        data['veto_first'] = 'team2'

        data['side_type'] = "standard"
        data['favored_percentage_team1'] = 50
        data['favored_percentage_team2'] = 50
        data['favored_percentage_text'] = "CSC Website Predictions"

        data['maplist'] = ['de_dust2', 'de_inferno', 'de_mirage', 'de_nuke', 'de_overpass', 'de_train', 'de_vertigo']
        # todo: test tag, name, country code is 2 letter country
        # get away team checkin
        awayplayers = []
        awaycheck = MatchCheckIn.objects.get(match=match, team=match.awayteam)
        for x in awaycheck.players.all():
            # get each player that checked in steamid
            try:
                temp = UserProfile.objects.get(user=x)
                awayplayers.add(temp.steamid64)
            except:
                messages.error(request, "An error occurred finding a checkedin players profile/steamid")
                return redirect('matches:detail', pk=match.pk)
        # get home team checkin
        homecheck = MatchCheckIn.objects.get(match=match, team=match.hometeam)
        homeplayers = []
        for y in homecheck.players.all():
            # get each player that checked in steamid
            try:
                temp = UserProfile.objects.get(user=y)
                homeplayers.add(temp.steamid64)
            except:
                messages.error(request, "An error occurred finding a checkedin players profile/steamid")
                return redirect('matches:detail', pk=match.pk)
        if match.awayteam.country == "":
            data['team1'] = {'name': match.awayteam.name, 'tag': match.awayteam.tag, 'flag': "US"}
            messages.error(request, "Away Team has no country set, using US as default")
        else:
            data['team1'] = {'name': match.awayteam.name, 'tag': match.awayteam.tag,
                             'flag': match.awayteam.country.code}
        data['team1']['players'] = {}
        data['team2'] = {'name': match.awayteam.name, 'tag': match.awayteam.tag, 'flag': match.awayteam.country.code}
        data['team2']['players'] = {}
        for x in awayplayers:
            data['team1']['players'][x.steamid64] = x.alternate_name
        for y in homeplayers:
            data['team2']['players'][y.steamid64] = y.alternate_name
