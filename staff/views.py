from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View, DetailView

from matches.models import MatchReport, MatchDispute
from profiles.forms import SortForm
from profiles.models import BannedUser
from staff.forms import *
from store.models import Transaction, Transfer, Product
from support.models import Ticket, TicketComment
from teams.models import TeamInvite
from . import calculaterank


def staffindex(request):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        ticket = Ticket.objects.all()
        news = Post.objects.all()
        teams = Team.objects.all()
        numusers = len(UserProfile.objects.all())
        tournaments = SingleEliminationTournament.objects.all()
        return render(request, 'staff/staffindex.html', {'ticket': ticket, 'news': news, 'teams': teams,
                                                         'tournaments': tournaments, 'numusers': numusers})


# start users

def users(request):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        object_list = UserProfile.objects.get_queryset().order_by('id')
        paginator = Paginator(object_list, 20)
        numusers = len(UserProfile.objects.all())
        page = request.GET.get('page')
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            # if it aint no integer deliver the first page
            users = paginator.page(1)
        except EmptyPage:
            # if the page is out of range deliver last page of results
            users = paginator.page(paginator.num_pages)
        context = {'page': page, 'userprofiles': users,
                   'bannedusernames': BannedUser.objects.values_list('user', flat=True),
                   'bannedips': BannedUser.objects.values_list('ip', flat=True), 'numusers': numusers,
                   'request': request}
        return render(request, 'staff/users.html', context)


def searchusers(request):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        query = request.GET.get('q')
        if query:
            return render(request, 'staff/users.html',
                          {'userprofiles': UserProfile.objects.filter
                          (Q(user__username__icontains=query) | Q(user__email__icontains=query)),
                           'bannedusers': list(BannedUser.objects.all())})
        else:
            return redirect('staff:users')


def banuser(request, urlusername):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        buser = User.objects.get(username=urlusername)
        b = BannedUser(user=buser, ip='999.999.999.999')
        b.save()
        messages.success(request, 'User ' + urlusername + ' has been banned')
        return redirect('staff:users')


def unbanuser(request, urlusername):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        buser = User.objects.get(username=urlusername)
        b = BannedUser.objects.get(user=buser)
        b.delete()
        messages.success(request, 'User ' + urlusername + ' has been unbanned')
        return redirect('staff:users')


def banip(request, urlusername):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        buser = User.objects.get(username=urlusername)
        buserprofile = UserProfile.objects.get(user__username=urlusername)
        if (buserprofile.ip == '127.0.0.1') or (buserprofile.ip == '0.0.0.0') or (buserprofile.ip == '999.999.999.999'):
            messages.error(request, 'User has non-bannable IP')
            return redirect('staff:users')
        else:
            b = BannedUser(user=buser, ip=buserprofile.ip)
            b.save()
            messages.success(request, 'User ' + urlusername + ' has been banned')
            return redirect('staff:users')


def unbanip(request, urlusername):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        buserprofile = UserProfile.objects.get(user__username=urlusername)
        b = BannedUser.objects.get(ip=buserprofile.ip)
        b.delete()
        messages.success(request, 'User ' + urlusername + ' has been banned')
        return redirect('staff:users')


def getrank(request):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        allusers = UserProfile.objects.all()
        calculaterank.calculaterank()
        messages.success(request, "Calculated rank for %s users" % allusers.count())
        return redirect('staff:users')


def modifyuser(request, urlusername):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        if request.method == 'GET':
            userprofileobj = UserProfile.objects.get(user__username=urlusername)
            form = ModifyUserForm(instance=userprofileobj)
            return render(request, 'staff/modifyuser.html', {'form': form})
        else:
            userprofileobj = UserProfile.objects.get(user__username=urlusername)
            form = ModifyUserForm(request.POST, instance=userprofileobj)
            if form.is_valid():
                form.save()
                messages.success(request, 'User has been updated')
                return redirect('staff:users')


def userdetail(request, urlusername):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        if request.method == 'POST':
            userprofile = UserProfile.objects.get(user__username=urlusername)
            userprofile.profile_picture = ''
            userprofile.save()
            messages.success(request, "Removed profile picture")
            return redirect('staff:userdetail', urlusername=urlusername)

        else:
            userprofile = UserProfile.objects.get(user__username=urlusername)
            return render(request, 'staff/profile_detail.html', {'userprofile': userprofile})


def verify(request, urlusername):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        userprofile = UserProfile.objects.get(user__username=urlusername)
        userprofile.user_verified = not userprofile.user_verified
        userprofile.save()
        return redirect('staff:users')


# end users


# start tournaments

def add_teams(request, pk):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        if request.method == 'POST':
            tournament = SingleEliminationTournament.objects.get(pk=pk)
            form = AddTournamentTeamForm(request.POST)
            if form.is_valid():
                teamid = form.cleaned_data['teams']
                try:
                    tournament.teams.add(Team.objects.get(id=teamid))
                    tournament.save()
                    messages.success(request, 'The specified team has successfully been added to the tournament')
                except:
                    messages.error(request, 'An error has occured and the team was not added to the tournament')
                return redirect('staff:tournament_detail', pk)
        else:
            tournament = SingleEliminationTournament.objects.get(pk=pk)
            form = AddTournamentTeamForm()
            return render(request, 'staff/tournament_add_team.html', {'form': form, 'tournament': tournament})
        return render(request, 'staff/tournament_detail.html', {'tournament': tournament})


def tournaments(request):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        tournament_list = SingleEliminationTournament.objects.all().order_by('-id')
        return render(request, 'staff/tournaments.html', {'tournament_list': tournament_list})


def tournament_detail(request, pk):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        tournament = SingleEliminationTournament.objects.get(pk=pk)
        rounds = SingleTournamentRound.objects.filter(tournament=tournament).order_by('id')
        return render(request, 'staff/tournament_detail.html', {'tournament': tournament, 'rounds': rounds})


def round_detail(request, pk):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        tround = SingleTournamentRound.objects.get(pk=pk)
        matches = tround.matches.all().order_by('id')
        return render(request, 'staff/round_detail.html', {'round': tround, 'matches': matches})


def edit_round(request, pk):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        if request.method == 'POST':
            roundobj = SingleTournamentRound.objects.get(id=pk)
            form = EditRoundInfoForm(request.POST, instance=roundobj)
            if form.is_valid():
                form.save()
                messages.success(request, 'Round has been updated')
                for match in roundobj.matches.all():
                    match.update_info(roundobj)
                return redirect('staff:round_detail', pk)
        else:
            roundobj = SingleTournamentRound.objects.get(id=pk)
            form = EditRoundInfoForm(instance=roundobj)
            return render(request, 'staff/edit_round.html', {'form': form})


def tournament_matches(request, pk):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        tournament = SingleEliminationTournament.objects.get(pk=pk)


def edit_tournament(request, pk):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        if request.method == 'POST':
            tournamentobj = SingleEliminationTournament.objects.get(pk=pk)
            form = EditTournamentForm(request.POST, request.FILES, instance=tournamentobj)
            if form.is_valid():
                form.save()
                messages.success(request, 'Tournament has been updated')
                return redirect('staff:tournamentlist')
            else:
                return render(request, 'staff/edittournament.html', {'form': form})
        else:
            tournamentobj = SingleEliminationTournament.objects.get(pk=pk)
            if not tournamentobj.bracket_generated:
                form = EditTournamentForm(instance=tournamentobj)
                return render(request, 'staff/edittournament.html', {'form': form, 'pk': pk})
            else:
                messages.error(request, 'You cannot edit a launched tournament')
                return redirect('staff:tournamentlist')


def create_tournament(request):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        if request.method == 'GET':
            form = CreateTournamentForm()
            return render(request, 'staff/createtournament.html', {'form': form})
        else:
            form = CreateTournamentForm(request.POST, request.FILES)
            if form.is_valid():
                tournament = form.instance
                tournament.save()
                messages.success(request, 'Created tournament')
                return redirect('staff:tournament_detail', pk=tournament.id)
            else:
                form = CreateTournamentForm(request.POST)
                return render(request, 'staff/createtournament.html', {'form': form})


def generate_bracket(request, pk):  # Launch tournament
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        tournament = SingleEliminationTournament.objects.get(pk=pk)
        if tournament.bracket_generated:
            messages.error(request, message='The bracket is already generated.')
            return redirect('staff:tournamentlist')
        else:
            calculaterank.calculaterank()
            tournament.generate_rounds()
            tournament.generate_bracket()
            tournament.bracket_generated = True
            tournament.save()
            messages.success(request, "Bracket Generated")
            return redirect('staff:tournamentlist')


def delete_tournament(request, pk):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        tournament = SingleEliminationTournament.objects.get(pk=pk)
        tournament.delete()
        messages.success(request, "Tournament Deleted")
        return redirect('staff:tournamentlist')


def ruleset_list(request):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        if request.method == 'GET':
            rulesets = SingleTournamentRuleset.objects.all().order_by('id')
            return render(request, 'staff/ruleset_list.html', {'rulesets': rulesets})
        else:
            rulesets = SingleTournamentRuleset.objects.all().order_by('id')
            return render(request, 'staff/ruleset_list.html', {'rulesets': rulesets})


def ruleset_create(request):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        if request.method == 'POST':
            form = SingleRulesetCreateForm(request.POST)
            if form.is_valid():
                ruleset = form.instance
                ruleset.creator = request.user
                ruleset.save()
                messages.success(request, 'Ruleset has been created!')
                return redirect('staff:tournamentrulesetlist')
            else:
                return render(request, 'staff/createruleset.html', {'form': form})
        else:
            form = SingleRulesetCreateForm(None)
            return render(request, 'staff/createruleset.html', {'form': form})


def ruleset_detail(request, pk):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        if request.method == 'POST':
            ruleset = SingleTournamentRuleset.objects.get(id=pk)
            return render(request, 'staff/ruleset_detail.html', {'ruleset': ruleset})
        else:
            ruleset = SingleTournamentRuleset.objects.get(id=pk)
            return render(request, 'staff/ruleset_detail.html', {'ruleset': ruleset})


def mikes_super_function(pk, currentround, nextround):
    tournament = SingleEliminationTournament.objects.get(pk=pk)
    currentround = SingleTournamentRound.objects.get(pk=currentround)
    nextround = SingleTournamentRound.objects.get(pk=nextround)

    matches = currentround.matches.all()
    bye2_count = 0

    for i in matches:
        if i.bye_2 is True and i.winner_id is None and i.hometeam_id is None and i.awayteam_id is None:
            # there are 2 bye teams, there won't be a winner
            bye2_count += 1
        elif i.completed is False:
            return False

        # elif i.winner_id is None:
        #   return False
    return bye2_count


def advance(request, pk):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        tournament = SingleEliminationTournament.objects.get(pk=pk)
        currentround = SingleTournamentRound.objects.get(tournament=pk, roundnum=tournament.current_round)
        try:
            nextround = SingleTournamentRound.objects.get(tournament=tournament, roundnum=tournament.current_round + 1)
        except:
            messages.warning(request, "All rounds are complete")
            tournament.active = False
            tournament.save()
            return redirect('staff:tournamentlist')
        matches = currentround.matches.all()
        for i in matches:
            if i.winner is None:
                if mikes_super_function(tournament.id, currentround.id, nextround.id) is False:
                    messages.error(request, "Some matches in the current round do not have a winner set")
                    return redirect('staff:tournamentlist')
                else:
                    mike = mikes_super_function(tournament.id, currentround.id, nextround.id)

            # if i.completed is False:
            # messages.error(request, 'There is a match that is not yet marked as completed in the current round')
            # return redirect('staff:tournamentlist')

        winners = []

        for i in matches:

            try:
                if i.winner is None:
                    winners.append('BYE TEAM')

                else:
                    winners.append(i.winner)
                    team = Team.objects.get(id=i.winner_id)
                    team.num_matchwin += 1
                    team.save()
                    team1 = Team.objects.get(id=i.loser_id)
                    team1.num_matchloss += 1
                    team1.save()
            except:
                pass

        # check to make sure mike +

        i = 0
        while i < len(winners):
            if winners[i] is 'BYE TEAM':
                newmatch = Match(game=tournament.game, platform=tournament.platform, hometeam=winners[i + 1])

            elif winners[i + 1] is 'BYE TEAM':
                newmatch = Match(game=tournament.game, platform=tournament.platform,
                                 awayteam=winners[i])
            else:
                newmatch = Match(game=tournament.game, platform=tournament.platform,
                                 awayteam=winners[i], hometeam=winners[i + 1])
            newmatch.save()
            nextround.matches.add(newmatch)
            i += 2

        tournament.current_round = tournament.current_round + 1
        tournament.save()
        messages.success(request, "Advanced to next round")
        return redirect('staff:tournamentlist')


class DeclareTournamentWinner(View):
    template_name = 'staff/winner_declare.html'

    def get(self, request, pk):
        user = UserProfile.objects.get(user__username=request.user.username)
        allowed = ['superadmin', 'admin']
        if user.user_type not in allowed:
            return render(request, 'staff/permissiondenied.html')
        else:
            form = DeclareTournamentWinnerForm
            return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        user = UserProfile.objects.get(user__username=request.user.username)
        allowed = ['superadmin', 'admin']
        if user.user_type not in allowed:
            return render(request, 'staff/permissiondenied.html')
        else:
            tournament = SingleEliminationTournament.objects.get(pk=pk)
            tournament_teams = list(tournament.teams.all())
            form = DeclareTournamentWinnerForm(request.POST)

            if form.cleaned_data['third'] is not None:
                first = Team.objects.get(id=form.data['winner'])
                second = Team.objects.get(id=form.data['second'])
                third = Team.objects.get(id=form.data['third'])

                if (first in tournament_teams) and (second in tournament_teams) and (third in tournament_teams):
                    tournament.winner = first
                    tournament.second = second
                    tournament.third = third

                    # Add losses to all other teams in tournament
                    tournament_teams.remove(first)
                    tournament_teams.remove(second)
                    tournament_teams.remove(third)
                    for team in tournament_teams:
                        team.num_matchloss += 1
                        team.save()
                    # End adding losses

                    tournament.active = False

                    tournament.save()
                    first.num_tournywin += 1
                    second.num_tournywin += 1
                    third.num_tournywin += 1
                    first.save()
                    second.save()
                    third.save()
                    messages.success(request, 'Set tournament winner')
                    return redirect('staff:tournamentlist')
                else:
                    form = DeclareTournamentWinnerForm
                    messages.error(request, 'One or more teams selected are not in this tournament')
                    return render(request, self.template_name, {'form': form})
            else:
                first = Team.objects.get(id=form.data['winner'])
                second = Team.objects.get(id=form.data['second'])

                if (first in tournament_teams) and (second in tournament_teams):
                    tournament.winner = first
                    tournament.second = second

                    # Add losses to all other teams in tournament
                    tournament_teams.remove(first)
                    tournament_teams.remove(second)
                    for team in tournament_teams:
                        team.num_matchloss += 1
                        team.save()
                    # End adding losses

                    tournament.active = False

                    tournament.save()
                    first.num_tournywin += 1
                    second.num_tournywin += 1
                    first.save()
                    second.save()
                    messages.success(request, 'Set tournament winner')
                    return redirect('staff:tournamentlist')
                else:
                    form = DeclareTournamentWinnerForm
                    messages.error(request, 'One or more teams selected are not in this tournament')
                    return render(request, self.template_name, {'form': form})


# end tournament section

# start matches section


def matches_index(request):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        matches_list = Match.objects.all().order_by('-id')
        return render(request, 'staff/matches.html', {'matches_list': matches_list})


def match_detail(request, pk):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        match = Match.objects.get(pk=pk)
        if match.disputed:
            dispute = MatchDispute.objects.get(match=match)
            return render(request, 'staff/match_detail.html', {'match': match, 'dispute': dispute})
        else:
            return render(request, 'staff/match_detail.html', {'match': match})


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
                return render(request, 'staff/match_edit.html', {'form': form})
        else:
            matchobj = Match.objects.get(pk=pk)
            form = EditMatchForm(instance=matchobj)
            return render(request, 'staff/match_edit.html', {'form': form, 'pk': pk})


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
        return render(request, 'staff/dispute_detail.html', {'dispute': dispute})


def gamelist(request):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        games = GameChoice.objects.all().order_by('id')
        return render(request, 'staff/game_list.html', {'games': games})


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
                return render(request, 'staff/editgame.html', {'form': form})
        else:
            game = GameChoice.objects.get(pk=pk)
            form = GameChoiceForm(instance=game)
            return render(request, 'staff/editgame.html', {'form': form, 'pk': pk})


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
            return render(request, 'staff/editgame.html', {'form': form})
        else:
            form = GameChoiceForm(request.POST, request.FILES)
            if form.is_valid():
                gamechoice = form.instance
                gamechoice.save()
                messages.success(request, 'Created Game')
                return redirect('staff:gamelist')
            else:
                form = GameChoiceForm(request.POST, request.FILES)
                return render(request, 'staff/editgame.html', {'form': form})


def platformlist(request):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        platforms = PlatformChoice.objects.all().order_by('id')
        return render(request, 'staff/platform_list.html', {'platforms': platforms})


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
                return render(request, 'staff/editplatform.html', {'form': form})
        else:
            platform = PlatformChoice.objects.get(pk=pk)
            form = PlatformChoiceForm(instance=platform)
            return render(request, 'staff/editplatform.html', {'form': form, 'pk': pk})


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
            return render(request, 'staff/editplatform.html', {'form': form})
        else:
            form = PlatformChoiceForm(request.POST, request.FILES)
            if form.is_valid():
                platformchoice = form.instance
                platformchoice.save()
                messages.success(request, 'Created Game')
                return redirect('staff:platformlist')
            else:
                form = GameChoiceForm(request.POST, request.FILES)
                return render(request, 'staff/editplatform.html', {'form': form})


def map_list(request):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        maps = MapChoice.objects.all().order_by('id')
        return render(request, 'staff/map_list.html', {'maps': maps})


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
                return render(request, 'staff/editmap.html', {'form': form})
        else:
            mapchoice = MapChoice.objects.get(pk=pk)
            form = MapChoiceForm(instance=mapchoice)
            return render(request, 'staff/editmap.html', {'form': form, 'pk': pk})


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
            return render(request, 'staff/editmap.html', {'form': form})
        else:
            form = MapChoiceForm(request.POST, request.FILES)
            if form.is_valid():
                mapchoice = form.instance
                mapchoice.save()
                messages.success(request, 'Created Map')
                return redirect('staff:map_list')
            else:
                form = GameChoiceForm(request.POST, request.FILES)
                return render(request, 'staff/editmap.html', {'form': form})


def map_pool_list(request):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        mappools = MapPoolChoice.objects.all().order_by('id')
        return render(request, 'staff/map_pool_list.html', {'mappools': mappools})


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
                return render(request, 'staff/editmappool.html', {'form': form})
        else:
            mappoolchoice = MapPoolChoice.objects.get(pk=pk)
            maps = mappoolchoice.maps.all()
            form = MapPoolChoiceForm(instance=mappoolchoice)
            return render(request, 'staff/editmappool.html', {'form': form, 'maps':maps, 'pk': pk})


def add_map_to_pool(request, pk):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        mappool = MapPoolChoice.objects.get(pk=pk)
        maps = MapChoice.objects.filter(game=mappool.game)
        if request.method == 'POST':
            form = AddMapForm(maps, request.POST)
            mapobj = form.data['mapobj']
            mappool.add_map(mapobj)
            messages.success(request, 'Map has been added to the pool')
            return redirect('staff:map_pool_detail', pk=pk)

        else:
            form = AddMapForm(maps)
            return render(request, 'staff/add_map.html', {'form': form, 'pk': pk})


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
            return render(request, 'staff/editmappool.html', {'form': form})
        else:
            form = MapPoolChoiceForm(request.POST, request.FILES)
            if form.is_valid():
                mappoolchoice = form.instance
                mappoolchoice.save()
                messages.success(request, 'Created Map Pool')
                return redirect('staff:map_pool_list')
            else:
                form = GameChoiceForm(request.POST, request.FILES)
                return render(request, 'staff/editmappool.html', {'form': form})

# end matches section


# start support section


def tickets(request):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        if request.method == 'GET':
            form = TicketSearchForm
            ticket_list = Ticket.objects.filter(status__lte=2).order_by('-id')
            return render(request, 'staff/tickets.html', {'form': form, 'ticket_list': ticket_list})

        elif request.method == 'POST':
            form = TicketSearchForm(request.POST)
            ticket_list = Ticket.objects.filter(status__lte=2).order_by('-id')
            if request.POST.get('showClosed'):
                ticket_list = Ticket.objects.all().order_by('-id')
            if request.POST.get('searchQuery'):
                query = request.POST.get('searchQuery')
                try:
                    ticket_list = Ticket.objects.filter(pk=query).order_by('-id')
                except ValueError:
                    ticket_list = Ticket.objects.filter(Q(text__contains=query) |
                                                        Q(creator__username__contains=query)).order_by('-id')
            return render(request, 'staff/tickets.html', {'form': form, 'ticket_list': ticket_list})


def ticket_category_list(request):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        cats = TicketCategory.objects.all()
        return render(request, 'staff/ticket_cats.html', {'cats': cats})


class TicketCategoryCreate(View):
    form_class = TicketCategoryCreateForm
    template_name = 'staff/ticket_cat_create.html'

    def get(self, request):
        user = UserProfile.objects.get(user__username=request.user.username)
        allowed = ['superadmin', 'admin']
        if user.user_type not in allowed:
            return render(request, 'staff/permissiondenied.html')
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        user = UserProfile.objects.get(user__username=request.user.username)
        allowed = ['superadmin', 'admin']
        if user.user_type not in allowed:
            return render(request, 'staff/permissiondenied.html')
        form = self.form_class(request.POST)

        if form.is_valid():
            cat = form.instance
            cat.name = form.cleaned_data['name']
            cat.priority = form.cleaned_data['priority']
            cat.save()
            messages.success(self.request, 'Ticket Category successfully added')
            return redirect('staff:ticket_categories')
        else:
            messages.error(self.request, 'An error occurred')
            return render(request, self.template_name, {'form': form})


def ticket_cat_delete(request, pk):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        cat = TicketCategory.objects.get(pk=pk)
        # cat = get_object_or_404(TicketCategory, pk=pk)
        cat.delete()
        # cat.save()
        messages.success(request, 'Successfully deleted ticket category')
        return redirect('staff:ticket_categories')


class TicketDetail(DetailView):
    model = Ticket
    template_name = 'staff/ticket_detail.html'
    form1 = TicketCommentCreateForm()
    form1_class = TicketCommentCreateForm
    form2 = TicketStatusChangeForm()
    form2_class = TicketStatusChangeForm

    def get(self, request, **kwargs):
        user = UserProfile.objects.get(user__username=request.user.username)
        allowed = ['superadmin', 'admin']
        if user.user_type not in allowed:
            return render(request, 'staff/permissiondenied.html')
        form1 = self.form1_class(None)
        form2 = self.form2_class(None)
        pk = self.kwargs['pk']
        ticket = Ticket.objects.get(id=pk)
        comments = TicketComment.objects.filter(ticket=pk).order_by('id')
        return render(request, self.template_name, {'form': form1, 'form2': form2, 'x': pk,
                                                    "ticket": ticket, "comments": comments})

    def get_context_date(self, **kwargs):
        context = super(TicketDetail, self).get_context_data(**kwargs)
        context['form'] = self.form
        return context

    def post(self, request, *args, **kwargs):
        user = UserProfile.objects.get(user__username=request.user.username)
        allowed = ['superadmin', 'admin']
        if user.user_type not in allowed:
            return render(request, 'staff/permissiondenied.html')
        if 'post_comment' in request.POST:
            self.form1 = TicketCommentCreateForm(request.POST)
            if self.form1.is_valid():
                self.form1_valid(self.form1)
                return redirect(reverse('staff:ticket_detail', args=[self.kwargs['pk']]))
            return super(TicketDetail, self).get(request, *args, **kwargs)

        if 'change_status' in request.POST:
            self.form2 = TicketStatusChangeForm(request.POST, instance=Ticket.objects.get(pk=self.kwargs['pk']))
            if self.form2.is_valid():
                self.status_form_valid(self.form2)
                return redirect(reverse('staff:ticket_detail', args=[self.kwargs['pk']]))
            return super(TicketDetail, self).get(request, *args, **kwargs)

    def form1_valid(self, form1):
        comment = form1.instance
        comment.author = self.request.user
        comment.ticket = Ticket.objects.get(id=self.kwargs['pk'])
        comment.save()
        messages.success(self.request, 'Your response has been successfully added to the ticket.')

    def status_form_valid(self, form2):
        ticket = form2.instance
        ticket.save()
        messages.success(self.request, 'Ticket successfully updated.')

    def get_queryset(self):
        return Ticket.objects.filter(creator=self.request.user)


class TicketCommentCreate(View):
    form_class = TicketCommentCreateForm
    template_name = 'staff/ticketcomment.html'

    def get(self, request, pk):
        user = UserProfile.objects.get(user__username=request.user.username)
        allowed = ['superadmin', 'admin']
        if user.user_type not in allowed:
            return render(request, 'staff/permissiondenied.html')
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        user = UserProfile.objects.get(user__username=request.user.username)
        allowed = ['superadmin', 'admin']
        if user.user_type not in allowed:
            return render(request, 'staff/permissiondenied.html')
        form = self.form_class(request.POST)

        if form.is_valid():
            comment = form.instance
            comment.ticket = Ticket.objects.get(pk=pk)
            comment.author = self.request.user
            comment.comment = form.cleaned_data['comment']
            comment.save()
            messages.success(self.request, 'Comment successfully added')
            return redirect('staff:tickets')
        else:
            messages.error(self.request, 'An error occurred')
            return render(request, self.template_name, {'form': form})


# end support section

# start static info section


def pages(request):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        if request.method == 'POST':
            staticinfoobj = StaticInfo.objects.get(pk=1)
            form = StaticInfoForm(request.POST, request.FILES, instance=staticinfoobj)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your information has been updated')
                return redirect('staff:pages')
            else:
                messages.error(request, "Something went horribly wrong (this shouldn't be seen)")
                return render(request, 'staff/staticinfo.html', {'form': form})
        else:
            staticinfoobj = StaticInfo.objects.get(pk=1)
            form = StaticInfoForm(instance=staticinfoobj)
            return render(request, 'staff/staticinfo.html', {'form': form, 'tenant': request.tenant})


def partnerlist(request):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        partner_list = Partner.objects.all().order_by('id')
        return render(request, 'staff/partnerslist.html', {'partner_list': partner_list})


def createpartner(request):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        if request.method == 'POST':
            form = PartnerForm(request.POST, request.FILES)
            if form.is_valid():
                # partner = form.instance
                # partner.author = User.objects.get(username=request.user.username)
                # partner.save()
                form.save()
                messages.success(request, 'Your partner has been created')
                return redirect('staff:partner_list')
            else:
                return render(request, 'staff/partnercreate.html', {'form': form})
        else:
            form = PartnerForm(None)
            return render(request, 'staff/partnercreate.html', {'form': form})


def partner_detail(request, pk):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        if request.method == 'POST':
            partner = Partner.objects.get(pk=pk)
            form = PartnerForm(request.POST, request.FILES, instance=partner)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your information has been updated')
                return redirect('staff:partner_list')
            else:
                return render(request, 'staff/partnercreate.html', {'form': form})
        else:
            partner = Partner.objects.get(pk=pk)
            form = PartnerForm(instance=partner)
            return render(request, 'staff/partnercreate.html', {'form': form})


# end static info section


# start news section

def news_list(request):
    # get all teh news articles
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        news_list = Post.objects.all().order_by('-id')
        return render(request, 'staff/news_list.html', {'news_list': news_list})


def create_article(request):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        if request.method == 'POST':
            form = ArticleCreateForm(request.POST, request.FILES)
            if form.is_valid():
                article = form.instance
                article.author = User.objects.get(username=request.user.username)
                article.save()
                form.save()
                messages.success(request, 'Your post has been created')
                return redirect('staff:news_list')
            else:
                return render(request, 'staff/create_article.html', {'form': form})
        else:
            form = ArticleCreateForm(None)
            return render(request, 'staff/create_article.html', {'form': form})


def detail_article(request, pk):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        article = Post.objects.get(id=pk)
        return render(request, 'staff/news_detail.html', {'article': article})


def edit_post(request, pk):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        if request.method == 'GET':
            article = get_object_or_404(Post, pk=pk)
            form = EditNewsPostForm(instance=article)
            return render(request, 'staff/edit_article.html', {'form': form})
        else:
            article = get_object_or_404(Post, pk=pk)
            form = EditNewsPostForm(request.POST, instance=article)
            if form.is_valid():
                post = form.instance
                post.author = request.user
                post.save()
                messages.success(request, "Updated post")
                return redirect('staff:detail_article', pk=pk)
            else:
                return render(request, 'staff/edit_article.html', {'form': form})


def delete_article(request, pk):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        article = Post.objects.get(pk=pk)
        article.delete()
        messages.success(request, 'Post has been deleted')
        return redirect('staff:news_index')


# end news section

# start store section


def store_index(request):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        if request.method == 'GET':
            products = len(Product.objects.all())
            transactions = len(Transaction.objects.all())
            transfers = len(Transfer.objects.all())
            return render(request, 'staff/store.html',
                          {'products': products, 'transactions': transactions, 'transfers': transfers})


class TransactionView(View):
    template_name = 'staff/transaction_list.html'
    form_class = SortForm

    def get(self, request, **kwargs):
        user = UserProfile.objects.get(user__username=request.user.username)
        allowed = ['superadmin', 'admin']
        if user.user_type not in allowed:
            return render(request, 'staff/permissiondenied.html')
        transaction_list = Transaction.objects.order_by('date')  # sort by date default
        form = self.form_class(None)
        return render(request, self.template_name, {'transaction_list': transaction_list, 'form': form})

    def post(self, request):
        user = UserProfile.objects.get(user__username=request.user.username)
        allowed = ['superadmin', 'admin']
        if user.user_type not in allowed:
            return render(request, 'staff/permissiondenied.html')
        form = self.form_class(request.POST)


class TransferView(View):
    template_name = 'staff/transfer_list.html'

    def get(self, request, **kwargs):
        user = UserProfile.objects.get(user__username=request.user.username)
        allowed = ['superadmin', 'admin']
        if user.user_type not in allowed:
            return render(request, 'staff/permissiondenied.html')

        query = request.GET.get('q')
        if query:
            transfer_list = Transfer.objects.filter(
                Q(origin__contains=query)).order_by('-date')
            return render(request, self.template_name, {'transfer_list': transfer_list})
        else:
            transfer_list = Transfer.objects.order_by('-date')  # sort by username default
            return render(request, self.template_name, {'transfer_list': transfer_list})


def products(request):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        if request.method == 'GET':
            product_list = Product.objects.all().order_by('id')
            return render(request, 'staff/product_list.html', {'product_list': product_list})


def product_detail(request, pk):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        if request.method == 'GET':
            product = Product.objects.get(id=pk)
            return render(request, 'staff/product_detail.html', {'product': product, 'pk': pk})


def create_product(request):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        if request.method == 'GET':
            form = CreateProductForm(None)
            return render(request, 'staff/create_product.html', {'form': form})
        else:
            form = CreateProductForm(request.POST)
            if form.is_valid():
                product = form.instance
                product.business = settings.PAYPAL_EMAIL
                product.save()
                return redirect('staff:product_detail', pk=product.id)
            else:
                return render(request, 'staff/create_product.html', {'form': form})


def edit_product(request, pk):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        if request.method == 'GET':
            form = CreateProductForm(instance=Product.objects.get(id=pk))
            return render(request, 'staff/edit_product.html', {'form': form, 'pk': pk})
        else:
            form = CreateProductForm(request.POST)
            if form.is_valid():
                product = Product.objects.get(id=pk)
                product.price = form.cleaned_data['price']
                product.amount = form.cleaned_data['amount']
                product.name = form.cleaned_data['name']
                product.item_name = form.cleaned_data['item_name']
                product.active = form.cleaned_data['active']
                product.save()
                return redirect('staff:product_detail', pk=product.id)
            else:
                return render(request, 'staff/edit_product.html', {'form': form, 'pk': pk})


def delete_product(request):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        if request.method == 'GET':
            form = DeleteProductForm(None)
            return render(request, 'staff/delete_product.html', {'form': form})
        else:
            form = DeleteProductForm(request.POST)
            if form.is_valid():
                product = Product.objects.get(price=form.data['price'], name=form.data['name'])
                messages.success(request, "Deleted product %s" % product.name)
                product.delete()
                return redirect('staff:index')  # need list view
            else:
                return render(request, 'staff/delete_product.html', {'form': form})


# end store section

# start teams section


def teams_index(request):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        teams_list = Team.objects.all().order_by('id')
        return render(request, 'staff/teams.html', {'teams_list': teams_list})


def teams_detail(request, pk):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        team = Team.objects.get(id=pk)
        players = TeamInvite.objects.filter(team=team, accepted=True).order_by('id')
        return render(request, 'staff/teams_detail.html', {'team': team, 'players': players, 'pk': pk})


def remove_user(request, pk):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        if request.method == 'POST':
            form = RemovePlayerFormPost(request.POST)
            invite = TeamInvite.objects.get(id=form.data['remove'])
            messages.success(request, 'Removed user %s from team' % invite)
            invite.delete()
            invites = TeamInvite.objects.filter(team_id=pk)
            if not invites.exists():
                team = Team.objects.get(id=pk)
                team.delete()
                messages.success(request, 'Deleted team due to the last user being removed')
                return redirect('staff:teamindex')
            else:
                return redirect('staff:team_detail', pk=pk)
        else:
            form = RemovePlayerForm(request, pk)
            return render(request, 'staff/remove_player.html', {'form': form, 'pk': pk})


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
