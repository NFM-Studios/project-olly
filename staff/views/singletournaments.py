from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import View

from staff.forms import *
from wagers.models import *
from .tools import calculaterank


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
            return render(request, 'staff/singletournaments/singletournament_add_team.html',
                          {'form': form, 'tournament': tournament})
        return render(request, 'staff/singletournaments/singletournament_detail.html', {'tournament': tournament})


def tournaments(request):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        tournament_list = SingleEliminationTournament.objects.all().order_by('-id')
        return render(request, 'staff/singletournaments/singletournament_list.html', {'tournament_list': tournament_list})


def tournament_detail(request, pk):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        tournament = SingleEliminationTournament.objects.get(pk=pk)
        rounds = SingleTournamentRound.objects.filter(tournament=tournament).order_by('id')
        return render(request, 'staff/singletournaments/singletournament_detail.html',
                      {'tournament': tournament, 'rounds': rounds})


def round_detail(request, pk):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        tround = SingleTournamentRound.objects.get(pk=pk)
        matches = tround.matches.all().order_by('id')
        return render(request, 'staff/singletournaments/round_detail.html', {'round': tround, 'matches': matches})


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
            return render(request, 'staff/singletournaments/round_edit.html', {'form': form})


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
                return render(request, 'staff/singletournaments/singletournament_edit.html', {'form': form})
        else:
            tournamentobj = SingleEliminationTournament.objects.get(pk=pk)
            if not tournamentobj.bracket_generated:
                form = EditTournamentForm(instance=tournamentobj)
                return render(request, 'staff/singletournaments/singletournament_edit.html', {'form': form, 'pk': pk})
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
            return render(request, 'staff/singletournaments/singletournament_create.html', {'form': form})
        else:
            form = CreateTournamentForm(request.POST, request.FILES)
            if form.is_valid():
                tournament = form.instance
                tournament.save()
                messages.success(request, 'Created tournament')
                return redirect('staff:tournament_detail', pk=tournament.id)
            else:
                form = CreateTournamentForm(request.POST)
                return render(request, 'staff/singletournaments/singletournament_create.html', {'form': form})


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
            calculaterank()
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
            return render(request, 'staff/singletournaments/ruleset_list.html', {'rulesets': rulesets})
        else:
            rulesets = SingleTournamentRuleset.objects.all().order_by('id')
            return render(request, 'staff/singletournaments/ruleset_list.html', {'rulesets': rulesets})


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
                return render(request, 'staff/singletournaments/ruleset_create.html', {'form': form})
        else:
            form = SingleRulesetCreateForm(None)
            return render(request, 'staff/singletournaments/ruleset_create.html', {'form': form})


def ruleset_detail(request, pk):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        if request.method == 'POST':
            ruleset = SingleTournamentRuleset.objects.get(id=pk)
            return render(request, 'staff/singletournaments/ruleset_detail.html', {'ruleset': ruleset})
        else:
            ruleset = SingleTournamentRuleset.objects.get(id=pk)
            return render(request, 'staff/singletournaments/ruleset_detail.html', {'ruleset': ruleset})


def mikes_super_function(currentround):
    currentround = SingleTournamentRound.objects.get(pk=currentround)

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
                if mikes_super_function(currentround.id) is False:
                    messages.error(request, "Some matches in the current round do not have a winner set")
                    return redirect('staff:tournamentlist')
                else:
                    mike = mikes_super_function(currentround.id)

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
                # disable user reports, its a bye match
                newmatch = Match(game=tournament.game, platform=tournament.platform, hometeam=winners[i + 1],
                                 disable_userreport=True, sport=tournament.sport)
            elif winners[i + 1] is 'BYE TEAM':
                # disable user reports, its a bye match
                newmatch = Match(game=tournament.game, platform=tournament.platform, sport=tournament.sport,
                                 awayteam=winners[i], disable_userreport=True)
            else:
                newmatch = Match(game=tournament.game, platform=tournament.platform,
                                 awayteam=winners[i], hometeam=winners[i + 1],
                                 # disable user match reports based on the field in the tournament
                                 disable_userreport=tournament.disable_userreport, sport=tournament.sport)
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
