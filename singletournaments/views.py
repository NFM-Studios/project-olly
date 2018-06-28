from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import SingleEliminationTournamentJoinGet, SingleEliminationTournamentJoinPost, SingleEliminationTournamentSort
from .models import SingleTournamentRound, SingleEliminationTournament, SingleTournamentTeam
from teams.models import TeamInvite, Team
from django.contrib import messages
from profiles.models import UserProfile
import datetime
from store.models import deduct_credits
import pytz
from django.shortcuts import get_object_or_404


class List(View):
    template_name = 'singletournaments/singletournament_list.html'
    form_class = SingleEliminationTournamentSort

    def get(self, request):
        form = self.form_class(None)
        tournament_list = SingleEliminationTournament.objects.all()
        return render(request, self.template_name, {'tournament_list': tournament_list, 'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        form.is_valid()
        platform = form.cleaned_data['platform']
        game = form.cleaned_data['game']
        if game == '0':
            tournament_list_ = SingleEliminationTournament.objects.filter(game=0)
        elif game == '1':
            tournament_list_ = SingleEliminationTournament.objects.filter(game=1)
        elif game == '2':
            tournament_list_ = SingleEliminationTournament.objects.filter(game=2)
        elif game == '3':
            tournament_list_ = SingleEliminationTournament.objects.filter(game=3)
        elif game == '4':
            tournament_list_ = SingleEliminationTournament.objects.filter(game=4)
        elif game == '5':
            tournament_list_ = SingleEliminationTournament.objects.filter(game=5)
        elif game == '6':
            tournament_list_ = SingleEliminationTournament.objects.filter(game=6)
        elif game == '7':
            tournament_list_ = SingleEliminationTournament.objects.filter(game=7)
        elif game == '8':
            tournament_list_ = SingleEliminationTournament.objects.filter(game=8)
        elif game == '9':
            tournament_list_ = SingleEliminationTournament.objects.filter(game=9)
        elif game == '10':
            tournament_list_ = SingleEliminationTournament.objects.filter(game=10)
        elif game == '11':
            tournament_list_ = SingleEliminationTournament.objects.filter(game=11)
        elif game == '12':
            tournament_list_ = SingleEliminationTournament.objects.filter(game=12)
        elif game == '13':
            tournament_list_ = SingleEliminationTournament.objects.filter(game=13)
        elif game == '14':
            tournament_list_ = SingleEliminationTournament.objects.filter(game=14)
        elif game == '15':
            tournament_list_ = SingleEliminationTournament.objects.all()

        if platform == '0':
            tournament_list1 = SingleEliminationTournament.objects.filter(platform=0)
        elif platform == '1':
            tournament_list1 = SingleEliminationTournament.objects.filter(platform=1)
        elif platform == '2':
            tournament_list1 = SingleEliminationTournament.objects.filter(platform=2)
        elif platform == '3':
            tournament_list1 = SingleEliminationTournament.objects.filter(platform=3)
        elif platform == '4':
            tournament_list1 = SingleEliminationTournament.objects.filter(platform=4)
        elif platform == '5':
            tournament_list1 = SingleEliminationTournament.objects.filter(platform=5)
        elif platform == '6':
            tournament_list1 = SingleEliminationTournament.objects.filter(platform=6)
        elif platform == '7':
            tournament_list1 = SingleEliminationTournament.objects.all()
        tournament_list = tournament_list1 & tournament_list_
        return render(request,  self.template_name, {'tournament_list': tournament_list, 'form': form})


class SingleTournamentJoin(View):
    template_name = 'singletournaments/singletournament_join.html'

    def get(self, request, pk):
        teaminvites = TeamInvite.objects.filter(user_id=request.user.id, hasPerms=True)
        if teaminvites.exists():
            form = SingleEliminationTournamentJoinGet(request)
            return render(request, self.template_name, {'form': form})
        else:
            messages.error(request, message="You aren't a captain or founder of any team!")
            return redirect('singletournaments:list')

    def post(self, request, pk):
        form = SingleEliminationTournamentJoinPost(request.POST)
        try:
            invite = TeamInvite.objects.get(user=request.user, team=form.data['teams'])
        except:
            messages.error(request, message="You aren't a captain or founder of this team")
            return redirect('singletournaments:list')
        if invite.hasPerms:
            tournament = SingleEliminationTournament.objects.get(id=self.kwargs['pk'])
            if tournament.teamformat == 0:
                players = 1
            elif tournament.teamformat == 1:
                players = 2
            elif tournament.teamformat == 2:
                players = 3
            elif tournament.teamformat == 3:
                players = 4
            elif tournament.teamformat == 4:
                players = 5
            elif tournament.teamformat == 5:
                players = 6
            team = Team.objects.get(id=int(form.data['teams']))
            users = TeamInvite.objects.filter(team=form.data['teams'])
            teams = tournament.teams.all()
            teameligible = False
            utc = pytz.UTC
            now = utc.localize(datetime.datetime.now())

            if tournament.open_register >= now:
                messages.error(request, 'Registration for this tournament is not open yet')
                return redirect('singletournaments:list')

            if tournament.close_register <= now:
                messages.error(request, 'Registration for this tournament is closed already')
                return redirect('singletournaments:list')

            if tournament.bracket_generated:
                messages.error(request, "The bracket has already been generated for this tournament, new teams aren't "
                                        "permitted")
                return redirect('singletournaments:list')

            if teams.count() >= tournament.size:
                messages.error(request, "This tournament is full")
                return redirect('singletournaments:list')
            for invite in users:
                user = UserProfile.objects.get(user_id=invite.user.id)
                if not user.xbl_verified or not user.psn_verified:
                    teameligible = False
                    messages.error(request, "One or more users does not have Xbox Live or PSN set")
                    return redirect('teams:list')
                elif int(user.credits) < int(tournament.req_credits):
                    teameligible = False
                    messages.error(request, "One or more players does not have enough credits")
                    return redirect('teams:list')
                else:
                    teameligible = True
                if not teameligible:
                    messages.error(request, "Not all members of your team are eligible to join")
            if len(users) > players:
                teameligible = False
            if not teameligible:
                messages.error(request, "There was an issue with team eligibility for this tournament")
                return redirect('teams:list')
            tournament_teams_query = tournament.teams.all()
            tournament_teams = []
            tournament_teams_invites_query = None
            tournament_teams_invites = []
            tournament_teams_users = []
            new_team = Team.objects.get(id=int(form.data['teams']))
            new_team_invites = TeamInvite.objects.filter(team=new_team)
            new_team_users = []
            for team in tournament_teams_query:
                tournament_teams.append(team)
            for team in tournament_teams:
                tournament_teams_invites_query = TeamInvite.objects.filter(team=team)
            try:
                for invite in tournament_teams_invites_query:
                    tournament_teams_invites.append(invite)
            except:
                pass
            try:
                for invite in tournament_teams_invites:
                    tournament_teams_users.append(invite.user)
            except:
                pass
            for invite in new_team_invites:
                new_team_users.append(invite.user)
            if new_team in tournament_teams:
                messages.error(request, message="This team is already in this tournament")
                return redirect('singletournaments:list')
            for user in new_team_users:
                if user in tournament_teams_users:
                    messages.error(request, "There is overlap between users in teams in the tournament")
                    return redirect('singletournaments:list')
            else:
                tournament.teams.add(new_team)
                for user in new_team_users:
                    deduct_credits(user, tournament.req_credits)
                tournament.save()
                tournament_team = SingleTournamentTeam(team_id=team.id, tournament_id=tournament.id)
                tournament_team.save()
                messages.success(request, message="Joined tournament")
                return redirect('singletournaments:list')
        else:
            messages.error(request, message="You can't join a tournament if you aren't the captain or founder")
            return redirect('singletournaments:list')


class SingleTournamentDetail(View):
    template_name = 'singletournaments/singletournament_detail.html'

    def get(self, request, **kwargs):
        pk = self.kwargs['pk']
        tournament = get_object_or_404(SingleEliminationTournament, id=pk)
        return render(request, self.template_name, {'pk': pk, 'tournament': tournament})


class SingleTournamentTeamsList(View):
    template_name = 'singletournaments/singletournament_teams.html'

    def get(self, request, **kwargs):
        pk = self.kwargs['pk']
        tournament = SingleEliminationTournament.objects.get(id=pk)
        teams = tournament.teams.all
        return render(request, self.template_name, {'x': pk, 'tournament': tournament, 'teams': teams})


class SingleTournamentRules(View):
    template_name = 'singletournaments/singletournament_rules.html'



class SingleTournamentMatchList(View):
    template_name = 'singletournaments/singletournament_matches.html'

    def get(self, request, **kwargs):
        pk = self.kwargs['pk']
        tournament = SingleEliminationTournament.objects.get(id=pk)
        if tournament.size == 4:
            # get only 2 round objects, and the matches inside them.
            round1 = SingleTournamentRound.objects.get(roundnum=1, tournament=tournament)
            round2 = SingleTournamentRound.objects.get(roundnum=2, tournament=tournament)
            round1matches = round1.matches.all()
            round2matches = round2.matches.all()

            return render(request, self.template_name, {'x': pk, 'tournament': tournament,
                                                        'round1matches':round1matches, 'round2matches':round2matches})

        elif tournament.size == 8:
            round1 = SingleTournamentRound.objects.get(roundnum=1, tournament=tournament)
            round2 = SingleTournamentRound.objects.get(roundnum=2, tournament=tournament)
            round3 = SingleTournamentRound.objects.get(roundnum=3, tournament=tournament)
            round1matches = round1.matches.all()
            round2matches = round2.matches.all()
            round3matches = round3.matches.all()
            return render(request, self.template_name, {'x': pk, 'tournament': tournament,
                                                        'round1matches': round1matches, 'round2matches': round2matches,
                                                        'round3matches': round3matches})

            # get 3 rounds
        elif tournament.size == 16:
            round1 = SingleTournamentRound.objects.get(roundnum=1, tournament=tournament)
            round2 = SingleTournamentRound.objects.get(roundnum=2, tournament=tournament)
            round3 = SingleTournamentRound.objects.get(roundnum=3, tournament=tournament)
            round4 = SingleTournamentRound.objects.get(roundnum=4, tournament=tournament)

            round1matches = round1.matches.all()
            round2matches = round2.matches.all()
            round3matches = round3.matches.all()
            round4matches = round4.matches.all()

            return render(request, self.template_name, {'x': pk, 'tournament': tournament,
                                                        'round1matches': round1matches, 'round2matches': round2matches,
                                                        'round3matches': round3matches, 'round4matches': round4matches})
            # get 4 rounds
        elif tournament.size == 32:
            round1 = SingleTournamentRound.objects.get(roundnum=1, tournament=tournament)
            round2 = SingleTournamentRound.objects.get(roundnum=2, tournament=tournament)
            round3 = SingleTournamentRound.objects.get(roundnum=3, tournament=tournament)
            round4 = SingleTournamentRound.objects.get(roundnum=4, tournament=tournament)
            round5 = SingleTournamentRound.objects.get(roundnum=5, tournament=tournament)

            round1matches = round1.matches.all()
            round2matches = round2.matches.all()
            round3matches = round3.matches.all()
            round4matches = round4.matches.all()
            round5matches = round5.matches.all()

            return render(request, self.template_name, {'x': pk, 'tournament': tournament,
                                                        'round1matches': round1matches, 'round2matches': round2matches,
                                                        'round3matches': round3matches, 'round4matches': round4matches,
                                                        'round5matches': round5matches})
            # get 5 rounds
        elif tournament.size == 64:
            round1 = SingleTournamentRound.objects.get(roundnum=1, tournament=tournament)
            round2 = SingleTournamentRound.objects.get(roundnum=2, tournament=tournament)
            round3 = SingleTournamentRound.objects.get(roundnum=3, tournament=tournament)
            round4 = SingleTournamentRound.objects.get(roundnum=4, tournament=tournament)
            round5 = SingleTournamentRound.objects.get(roundnum=5, tournament=tournament)
            round6 = SingleTournamentRound.objects.get(roundnum=6, tournament=tournament)

            round1matches = round1.matches.all()
            round2matches = round2.matches.all()
            round3matches = round3.matches.all()
            round4matches = round4.matches.all()
            round5matches = round5.matches.all()
            round6matches = round6.matches.all()

            return render(request, self.template_name, {'x': pk, 'tournament': tournament,
                                                        'round1matches': round1matches, 'round2matches': round2matches,
                                                        'round3matches': round3matches, 'round4matches': round4matches,
                                                        'round5matches': round5matches, 'round6matches': round6matches})
            # get 6 rounds
        elif tournament.size == 128:
            round1 = SingleTournamentRound.objects.get(roundnum=1, tournament=tournament)
            round2 = SingleTournamentRound.objects.get(roundnum=2, tournament=tournament)
            round3 = SingleTournamentRound.objects.get(roundnum=3, tournament=tournament)
            round4 = SingleTournamentRound.objects.get(roundnum=4, tournament=tournament)
            round5 = SingleTournamentRound.objects.get(roundnum=5, tournament=tournament)
            round6 = SingleTournamentRound.objects.get(roundnum=6, tournament=tournament)
            round7 = SingleTournamentRound.objects.get(roundnum=7, tournament=tournament)

            round1matches = round1.matches.all()
            round2matches = round2.matches.all()
            round3matches = round3.matches.all()
            round4matches = round4.matches.all()
            round5matches = round5.matches.all()
            round6matches = round6.matches.all()
            round7matches = round7.matches.all()

            return render(request, self.template_name, {'x': pk, 'tournament': tournament,
                                                        'round1matches': round1matches, 'round2matches': round2matches,
                                                        'round3matches': round3matches, 'round4matches': round4matches,
                                                        'round5matches': round5matches, 'round6matches': round6matches,
                                                        'round7matches': round7matches})
            #  get 7 rounds


class SingleTournamentBracket(View):

    def get(self, request, **kwargs):
        pk = self.kwargs['pk']
        winners = []
        completed = []
        doing = []
        matches = []
        tournament = SingleEliminationTournament.objects.get(id=pk)
        teams = tournament.teams.all()
        if tournament.bracket_generated:
            # show the right bracket
            if tournament.size == 4:
                # get 2 rounds to pass to the view
                template_name = 'singletournaments/singletournament_bracket4.html'

                round1 = SingleTournamentRound.objects.get(tournament=tournament, roundnum=1)
                round2 = SingleTournamentRound.objects.get(tournament=tournament, roundnum=2)

                round1matches = round1.matches.all()
                round2matches = round2.matches.all()

                return render(request, template_name,
                              {'x': pk, 'tournament': tournament, 'teams': teams, 'round1': round1,
                               'round2': round2, 'round1matches': round1matches, 'round2matches': round2matches})

            elif tournament.size == 8:
                # get 3 rounds to pass to the view
                template_name = 'singletournaments/singletournament_bracket8.html'
                round1 = SingleTournamentRound.objects.get(tournament=tournament, roundnum=1)
                round2 = SingleTournamentRound.objects.get(tournament=tournament, roundnum=2)
                round3 = SingleTournamentRound.objects.get(tournament=tournament, roundnum=3)

                round1matches = round1.matches.all()
                round2matches = round2.matches.all()
                round3matches = round3.matches.all()

                for match in round1matches:
                    if match.winner is not None:
                        matchid = match.id
                        winner = match.winner.id
                        completed.append(matchid)
                        winners.append(winner)
                        matches.append(matchid)
                        # there is a winner, celebrate
                    else:
                        # do some shit
                        matchid = match.id
                        matches.append(matchid)
                        doing.append(matchid)

                return render(request, template_name,
                              {'x': pk, 'tournament': tournament, 'teams': teams, 'round1': round1, 'round2': round2,
                               'round3': round3, 'round1matches': round1matches, 'round2matches': round2matches,
                               'round3matches': round3matches})

            elif tournament.size == 16:
                # get 4 rounds to pass to the view
                template_name = 'singletournaments/singletournament_bracket16.html'
                round1 = SingleTournamentRound.objects.get(tournament=tournament, roundnum=1)
                round2 = SingleTournamentRound.objects.get(tournament=tournament, roundnum=2)
                round3 = SingleTournamentRound.objects.get(tournament=tournament, roundnum=3)
                round4 = SingleTournamentRound.objects.get(tournament=tournament, roundnum=4)

                round1matches = round1.matches.all()
                round2matches = round2.matches.all()
                round3matches = round3.matches.all()
                round4matches = round4.matches.all()

                return render(request, template_name,
                              {'x': pk, 'tournament': tournament, 'teams': teams, 'round1': round1, 'round2': round2,
                               'round3': round3, 'round4': round4, 'round1matches': round1matches,
                               'round2matches': round2matches, 'round3matches': round3matches,
                               'round4matches': round4matches})

            elif tournament.size == 32:
                # get 5 rounds to pass to the view
                template_name = 'singletournaments/singletournament_bracket32.html'
                round1 = SingleTournamentRound.objects.get(tournament=tournament, roundnum=1)
                round2 = SingleTournamentRound.objects.get(tournament=tournament, roundnum=2)
                round3 = SingleTournamentRound.objects.get(tournament=tournament, roundnum=3)
                round4 = SingleTournamentRound.objects.get(tournament=tournament, roundnum=4)
                round5 = SingleTournamentRound.objects.get(tournament=tournament, roundnum=5)

                round1matches = round1.matches.all()
                round2matches = round2.matches.all()
                round3matches = round3.matches.all()
                round4matches = round4.matches.all()
                round5matches = round5.matches.all()

                return render(request, template_name,
                              {'x': pk, 'tournament': tournament, 'teams': teams, 'round1': round1, 'round2': round2,
                               'round3': round3, 'round4': round4, 'round5': round5,
                               'round1matches': round1matches, 'round2matches': round2matches,
                               'round3matches': round3matches, 'round4matches': round4matches,
                               'round5matches': round5matches})

            elif tournament.size == 64:
                # get 6 rounds to pass to the view
                template_name = 'singletournaments/singletournament_bracket64.html'
                round1 = SingleTournamentRound.objects.get(tournament=tournament, roundnum=1)
                round2 = SingleTournamentRound.objects.get(tournament=tournament, roundnum=2)
                round3 = SingleTournamentRound.objects.get(tournament=tournament, roundnum=3)
                round4 = SingleTournamentRound.objects.get(tournament=tournament, roundnum=4)
                round5 = SingleTournamentRound.objects.get(tournament=tournament, roundnum=5)
                round6 = SingleTournamentRound.objects.get(tournament=tournament, roundnum=6)

                round1matches = round1.matches.all()
                round2matches = round2.matches.all()
                round3matches = round3.matches.all()
                round4matches = round4.matches.all()
                round5matches = round5.matches.all()
                round6matches = round6.matches.all()

                return render(request, template_name,
                              {'x': pk, 'tournament': tournament, 'teams': teams, 'round1': round1, 'round2': round2,
                               'round3': round3, 'round4': round4, 'round5': round5, 'round6': round6,
                               'round1matches': round1matches, 'round2matches': round2matches,
                               'round3matches': round3matches, 'round4matches': round4matches,
                               'round5matches': round5matches, 'round6matches': round6matches})

            elif tournament.size == 128:
                # get 7 rounds to pass to the  view
                template_name = 'singletournaments/singletournament_bracket128.html'
                round1 = SingleTournamentRound.objects.get(tournament=tournament, roundnum=1)
                round2 = SingleTournamentRound.objects.get(tournament=tournament, roundnum=2)
                round3 = SingleTournamentRound.objects.get(tournament=tournament, roundnum=3)
                round4 = SingleTournamentRound.objects.get(tournament=tournament, roundnum=4)
                round5 = SingleTournamentRound.objects.get(tournament=tournament, roundnum=5)
                round6 = SingleTournamentRound.objects.get(tournament=tournament, roundnum=6)
                round7 = SingleTournamentRound.objects.get(tournament=tournament, roundnum=7)

                round1matches = round1.matches.all()
                round2matches = round2.matches.all()
                round3matches = round3.matches.all()
                round4matches = round4.matches.all()
                round5matches = round5.matches.all()
                round6matches = round6.matches.all()
                round7matches = round7.matches.all()

                return render(request, template_name,
                              {'x': pk, 'tournament': tournament, 'teams': teams, 'round1': round1, 'round2': round2,
                               'round3': round3, 'round4': round4, 'round5': round5, 'round6': round6, 'round7': round7,
                               'round1mathces': round1matches, 'round2matches': round2matches,
                               'round3matches': round3matches,
                               'round4matches': round4matches, 'round5matches': round5matches,
                               'round6matches': round6matches,
                               'round7matches': round7matches})
        else:
            # show some template that its not generated yet
            return render(request, 'singletournaments/no_bracket.html', {'tournament': tournament})
