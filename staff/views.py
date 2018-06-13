from django.contrib import messages
from django.shortcuts import render, redirect
from pages.models import StaticInfo
from staff.forms import StaticInfoForm, ArticleCreateForm, EditUserForm, TicketCommentCreateForm,\
    TicketStatusChangeForm, EditTournamentForm, DeclareMatchWinnerForm, DeclareMatchWinnerPost, DeclareTournamentWinnerForm
from profiles.models import UserProfile, BannedUser
from profiles.forms import SortForm
from django.contrib.auth.models import User
from django.urls import reverse
from django.views.generic import View, DetailView, CreateView
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from support.models import Ticket
from teams.models import Team
from matches.models import Match, MatchReport, MatchDispute
from news.models import Post, Comment, PublishedManager
from singletournaments.models import SingleEliminationTournament, SingleTournamentRound
from store.models import Transaction, Transfer
from support.models import Ticket, TicketComment


def staffindex(request):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        ticket = Ticket.objects.all()
        news = Post.objects.all()
        teams = Team.objects.all()
        tournaments = SingleEliminationTournament.objects.all()
        return render(request, 'staff/staffindex.html', {'ticket': ticket, 'news':news, 'teams': teams, 'tournaments': tournaments})


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
                   'bannedips': BannedUser.objects.values_list('ip', flat=True), 'numusers': numusers}
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
                print('form is not valid')
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
            form = EditTournamentForm(request.POST, instance=tournamentobj)
            if form.is_valid():
                form.save()
                messages.success(request, 'Tournament has been updated')
                return redirect('staff:tournamentlist')
            else:
                print('form is not valid')
        else:
            tournamentobj = SingleEliminationTournament.objects.get(pk=pk)
            form = EditTournamentForm(instance=tournamentobj)
            return render(request, 'staff/edittournament.html', {'form': form, 'pk': pk})


class CreateTournament(CreateView):
    form_class = EditTournamentForm
    template_name = 'staff/createtournament.html'

    def form_valid(self, form):
        tournament = form.instance
        tournament.save()
        tournament.generate_rounds()
        self.success_url = reverse('staff:tournamentlist')
        messages.success(self.request, 'Your tournament has been successfully created')
        return super(CreateTournament, self).form_valid(form)


def generate_bracket(request, pk):
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


def advance(request, pk):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        tournament = SingleEliminationTournament.objects.get(pk=pk)
        currentround = SingleTournamentRound.objects.get(tournament=pk, roundnum=tournament.current_round)
        nextround = SingleTournamentRound.objects.get(tournament=tournament, roundnum=tournament.current_round+1)
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
            team1 = Team.objects.get(id=i.loser_id)
            team1.num_matchloss += 1
            team.save()
            team1.save()

        for i in winners:
            newmatch = Match(game=tournament.game, platform=tournament.platform, hometeam=winners[0], awayteam=winners[1])
            newmatch.save()
            nextround.matches.add(newmatch)
            del winners[0]
            del winners[0]

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
            if (first in tournament_teams) and (second in tournament_teams):
                tournament.winner = first
                tournament.second = second
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


def match_delete_winner(request, pk):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        match = Match.objects.get(pk=pk)
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
        tickets = Ticket.objects.all()
        return render(request, 'staff/tickets.html', {'ticket_list': tickets})


class TicketDetail(DetailView):
    model = Ticket
    template_name = 'staff/ticket_detail.html'
    form1 = TicketCommentCreateForm()
    form1_class = TicketCommentCreateForm
    form2 = TicketStatusChangeForm()
    form2_class = TicketStatusChangeForm

    def get(self, request, **kwargs):
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
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        form = self.form_class(request.POST)

        if form.is_valid():
            comment = form.instance
            comment.ticket = Ticket.objects.get(pk=pk)
            comment.author = self.request.user
            comment.comment = form.cleaned_data['comment']
            comment.save()
            messages.success(self.request, 'Comment successfully added')
            return redirect('staff:tickets')

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
            form = StaticInfoForm(request.POST, instance=staticinfoobj)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your information has been updated')
                return redirect('staff:pages')
        else:
            staticinfoobj = StaticInfo.objects.get(pk=1)
            form = StaticInfoForm(instance=staticinfoobj)
            return render(request, 'staff/staticinfo.html', {'form': form})


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
            form = ArticleCreateForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Nice job boss, your post has been created')
                return redirect('staff:news_list')
        else:
            messages.error(request, "Gosh darnit, I messed up. I'm sorry")

# end news section

# start store section


class TransactionView(View):
    template_name = 'staff/transaction_list.html'
    form_class = SortForm

    def get(self, request, **kwargs):
        transaction_list = Transaction.objects.order_by('date')  # sort by date default
        form = self.form_class(None)
        return render(request, self.template_name, {'transaction_list': transaction_list, 'form': form})

    def post(self, request):
        form = self.form_class(request.POST)


class TransferView(View):
    template_name = 'staff/transfer_list.html'
    form_class = SortForm

    def get(self, request, **kwargs):
        transfer_list = Transfer.objects.order_by('date')  # sort by username default
        form = self.form_class(None)
        return render(request, self.template_name, {'transfer_list': transfer_list, 'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
