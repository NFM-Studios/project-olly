from django.contrib import messages
from django.shortcuts import render, redirect
from pages.models import StaticInfo
from staff.forms import StaticInfoForm, ArticleCreateForm, EditUserForm, TicketCommentCreateForm,\
    TicketStatusChangeForm, EditTournamentForm, DeclareMatchWinnerForm, DeclareMatchWinnerPost,\
    DeclareTournamentWinnerForm, TicketSearchForm, RemovePlayerForm, RemovePlayerFormPost, SingleRulesetCreateForm,\
    PartnerForm, EditNewsPostForm, CreateProductForm, DeleteProductForm, RemovePostForm, EditMatchForm, \
    CreateTournamentForm, ModifyUserForm, EditRoundInfoForm
from profiles.models import UserProfile, BannedUser
from profiles.forms import SortForm
from django.contrib.auth.models import User
from django.urls import reverse
from django.views.generic import View, DetailView, CreateView
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from teams.models import Team, TeamInvite
from matches.models import Match, MatchReport, MatchDispute
from news.models import Post, Comment, PublishedManager
from store.models import Transaction, Transfer, give_credits, Product
from singletournaments.models import SingleEliminationTournament, SingleTournamentRound, SingleTournamentRuleset
from support.models import Ticket, TicketComment
from django.shortcuts import get_object_or_404
from pages.models import Partner
from django.conf import settings
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


def edituser(request, urlusername):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        if request.method == 'POST':
            userprofileobj = UserProfile.objects.get(user__username=urlusername)
            form = EditUserForm(request.POST, instance=userprofileobj)
            if form.is_valid():
                form.save()
                messages.success(request, 'User type has been updated')
                return redirect('staff:users')
            else:
                return render(request, 'staff/edituser.html', {'form': form})
        else:
            userprofileobj = UserProfile.objects.get(user__username=urlusername)
            form = EditUserForm(instance=userprofileobj)
            return render(request, 'staff/edituser.html', {'form': form})


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
            form = ModifyUserForm(None)
            return render(request, 'staff/modifyuser.html', {'form': form})
        else:
            form = ModifyUserForm(request.POST)
            username = User.objects.get(username=urlusername)
            form.is_valid()
            creds = int(form.data['credits'])
            xp = int(form.data['xp'])
            user.xp += xp
            give_credits(username, creds)
            user.num_bronze += form.cleaned_data['bronze']
            user.num_silver += form.cleaned_data['silver']
            user.num_gold += form.cleaned_data['gold']
            user.current_earning += form.cleaned_data['earnings']
            user.save()
                                      cost=int(0.00), type='Bronze Trophies', staff=request.user.username)
            transaction = Transaction(num=form.cleaned_data['bronze'], account=user,
            transaction.save()
            transaction = Transaction(num=form.cleaned_data['silver'], account=user,
                                      cost=int(0.00), type='Silver Trophies', staff=request.user.username)
            transaction.save()
            transaction = Transaction(num=form.cleaned_data['gold'], account=user,
                                      cost=int(0.00), type='Gold Trophies', staff=request.user.username)
            transaction.save()
            transaction = Transaction(num=form.cleaned_data['earnings'], account=UserProfile.objects.get(user=username),
                                      cost=int(0.00), type='Account Earnings', staff=request.user.username)
            transaction.save()
            transaction = Transaction(num=xp, account=UserProfile.objects.get(user=username), cost=int(0.00),
                                      type='XP', staff=request.user.username)
            transaction.save()
            transaction = Transaction(num=creds, account=UserProfile.objects.get(user=username), cost=int(0.00),
                                      type='Credit', staff=request.user.username)
            transaction.save()
            messages.success(request, "Added credits/XP/trophies/earnings to %s" % urlusername)
            return redirect('staff:users')


def userdetail(request, urlusername):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
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
        return redirect('staff:index')

# end users


# start tournaments


def tournaments(request):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        tournament_list = SingleEliminationTournament.objects.all()
        return render(request, 'staff/tournaments.html', {'tournament_list': tournament_list})


def tournament_detail(request, pk):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        tournament = SingleEliminationTournament.objects.get(pk=pk)
        rounds = SingleTournamentRound.objects.filter(tournament = tournament)
        return render(request, 'staff/tournament_detail.html', {'tournament': tournament, 'rounds': rounds})


def round_detail(request, pk):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        tround = SingleTournamentRound.objects.get(pk=pk)
        matches = tround.matches.all()
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
            return render(request, 'staff/edit_round.html', {'form':form})


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
                form = EditTournamentForm(obj=tournamentobj)
                return render(request, 'staff/edittournament.html', {'form': form, 'pk': pk})
            else:
                messages.error(request, "The bracket has been generated, you cannot edit the tournament further")
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
            form = CreateTournamentForm(request.POST)
            if form.is_valid():
                tournament = form.instance
                tournament.save()
                messages.success(request, 'Created tournament')
                return redirect('staff:tournament_detail', pk=tournament.id)
            else:
                form = CreateTournamentForm(request.POST)
                return render(request, 'staff/createtournament.html', {'form':form})


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
            rulesets = SingleTournamentRuleset.objects.all()
            return render(request, 'staff/ruleset_list.html', {'rulesets': rulesets})
        else:
            rulesets = SingleTournamentRuleset.objects.all()
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


def advance(request, pk):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        tournament = SingleEliminationTournament.objects.get(pk=pk)
        currentround = SingleTournamentRound.objects.get(tournament=pk, roundnum=tournament.current_round)
        try:
            nextround = SingleTournamentRound.objects.get(tournament=tournament, roundnum=tournament.current_round+1)
        except:
            messages.warning(request, "All rounds are complete")
            tournament.active = False
            tournament.save()
            return redirect('staff:tournamentlist')
        matches = currentround.matches.all()
        for i in matches:
            if i.winner is None:
                messages.error(request, "The current round is not complete")
                return redirect('staff:tournamentlist')

        winners = []

        for i in matches:
            winners.append(i.winner)
            team = Team.objects.get(id=i.winner_id)
            team.num_matchwin += 1
            try:
                team1 = Team.objects.get(id=i.loser_id)
                team1.num_matchloss += 1
                team1.save()
            except:
                pass
            team.save()

        i = 0
        while i < len(winners):
            newmatch = Match(game=tournament.game, platform=tournament.platform,
                             awayteam=winners[i], hometeam=winners[i+1])
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


# end tournament section

# start matches section


def matches_index(request):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        matches_list = Match.objects.all()
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
                winner.num_matchwin += 1
                loser.num_matchloss += 1
                winner.save()
                loser.save()
                messages.success(request, "Winner declared")
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
            ticket_list = Ticket.objects.filter(status__lte=2)
            return render(request, 'staff/tickets.html', {'form': form, 'ticket_list': ticket_list})

        elif request.method == 'POST':
            form = TicketSearchForm(request.POST)
            ticket_list = Ticket.objects.filter(status__lte=2)
            if request.POST.get('showClosed'):
                ticket_list = Ticket.objects.all()
            if request.POST.get('searchQuery'):
                query = request.POST.get('searchQuery')
                try:
                    ticket_list = Ticket.objects.filter(pk=query)
                except ValueError:
                    ticket_list = Ticket.objects.filter(Q(text__contains=query) | Q(creator__username__contains=query))
            return render(request, 'staff/tickets.html', {'form': form, 'ticket_list': ticket_list})


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
        comments = TicketComment.objects.filter(ticket=pk)
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
        partner_list = Partner.objects.all()
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
                #partner = form.instance
                #partner.author = User.objects.get(username=request.user.username)
                #partner.save()
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
        news_list = Post.objects.all()
        return render(request, 'staff/news_list.html', {'news_list': news_list})


def news_index(request):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        return render(request, 'staff/news_index.html')


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


def remove_article(request):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        if request.method == 'GET':
            form = RemovePostForm(None)
            return render(request, 'staff/remove_post.html', {'form': form})
        else:
            form = RemovePostForm(request.POST)
            if form.is_valid():
                post = Post.objects.get(slug=form.data['slug'])
                messages.success(request, 'Removed post %s' % post.title)
                post.delete()
                return redirect('staff:news_index')
            else:
                return render(request, 'staff/remove_post.html', {'form': form})

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
    form_class = SortForm

    def get(self, request, **kwargs):
        user = UserProfile.objects.get(user__username=request.user.username)
        allowed = ['superadmin', 'admin']
        if user.user_type not in allowed:
            return render(request, 'staff/permissiondenied.html')
        transfer_list = Transfer.objects.order_by('date')  # sort by username default
        form = self.form_class(None)
        return render(request, self.template_name, {'transfer_list': transfer_list, 'form': form})

    def post(self, request):
        user = UserProfile.objects.get(user__username=request.user.username)
        allowed = ['superadmin', 'admin']
        if user.user_type not in allowed:
            return render(request, 'staff/permissiondenied.html')
        form = self.form_class(request.POST)


def products(request):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        if request.method == 'GET':
            product_list = Product.objects.all()
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
        players = TeamInvite.objects.filter(team=team, accepted=True)
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
        for i in allteams:
            i.get_rank()
        messages.success(request, "Calculated rank for %s teams" % allteams.count())

