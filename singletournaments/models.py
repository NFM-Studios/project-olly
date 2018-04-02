from django.db import models
from matches.settings import GAME_CHOICES, PLATFORMS_CHOICES, TEAMFORMAT_CHOICES, MAPFORMAT_CHOICES
from matches.models import Match
# from matches.models import Ruleset
from teams.models import Team
from random import *

SIZE_CHOICES = (
    (4, 4),
    (8, 8),
    (16, 16),
    (32, 32),
    (64, 64),
    (128, 128),
)


class SingleEliminationTournament(models.Model):
    name = models.CharField(max_length=50, blank=False, default='No name provided', unique=True)
    # I know we need the team format, ex 1v1, 2v2, 3v3, 4v4, 5v5, 6v6
    teamformat = models.SmallIntegerField(choices=TEAMFORMAT_CHOICES, default=1)
    # by default its a best of 1. Not sure if we need this here. Finals might be best of 3, etc in
    # the future possibly. TBD. For now this will work though.
    bestof = models.SmallIntegerField(choices=MAPFORMAT_CHOICES, default=0)

    # by default the tournament is not active. an admin has to activate it in order for it to be public
    active = models.BooleanField(default=False)

    # when does registration open, and when does it close? specified when created in staff panel
    open_register = models.DateTimeField()
    # dont allow people to join once registration is closed
    close_register = models.DateTimeField()

    # the time the specific tournament object was created
    created = models.DateTimeField(auto_now_add=True)
    # last time an admin updated something
    updated = models.DateTimeField(auto_now=True)

    req_credits = models.PositiveSmallIntegerField(default=0)

    # game and platform it will be played on
    platform = models.SmallIntegerField(choices=PLATFORMS_CHOICES, default=0)
    game = models.SmallIntegerField(choices=GAME_CHOICES, default=0)

    # when will the first round of matches start?
    start = models.DateTimeField()

    # all the teams that are in the event. elgibility happens inside the view, when they try to register @ben told me how to do this mtm field, i forgot
    teams = models.ManyToManyField(Team, blank=True)

    # specify the winning team when they are declared
    winner = models.ForeignKey(Team, related_name='winningteam', on_delete=models.CASCADE, blank=True, null=True)

    # specify second place, just for storage and future reference
    second = models.ForeignKey(Team, related_name='secondplaceteam', on_delete=models.CASCADE, blank=True, null=True)

    # specify how many teams the event will be capped at, and the size of the bracket
    size = models.PositiveSmallIntegerField(default=32, choices=SIZE_CHOICES)

    # the prizes that they will win, defined in admin panel. 3rd place isnt really needed..... just first and second...
    prize1 = models.CharField(default='no prize specified', max_length=50)
    prize2 = models.CharField(default='no prize specified', max_length=50)
    prize3 = models.CharField(default='no prize specified', max_length=50)

    # need to figure out how we will work rules
    # rules = models.ForeignKey(Ruleset, related_name='tournamentrules', on_delete=models.CASCADE, blank=False, null=True)

    def __str__(self):
        # pk = self.kwargs['pk']
        # tournament = SingleEliminationTournament.objects.get(id=pk)

        if self.platform == 0:
            platform = "Playstation"
        elif self.platform == 1:
            platform = "XBOX One"
        elif self.platform == 2:
            platform = "PC"
        elif self.platform == 3:
            platform = "Mobile"
        elif self.platform == 4:
            platform = "Nintendo Switch"
        elif self.platform == 5:
            platform = "Playstation"
        elif self.platform == 6:
            platform = "XBOX 360"

        if self.teamformat == 0:
            format = "1v1"
        elif self.teamformat == 1:
            format = "2v2"
        elif self.teamformat == 2:
            format = "3v3"
        elif self.teamformat == 3:
            format = "4v4"
        elif self.teamformat == 4:
            format = "5v5"
        elif self.teamformat == 5:
            format = "6v6"

        if self.game == 0:
            game = 'No Game Set'
        elif self.game == 1:
            game = 'Call of Duty: Black Ops 3'
        elif self.game == 2:
            game = 'Call of Duty WWII'
        elif self.game == 3:
            game = 'Fortnite'
        elif self.game == 4:
            game = 'Destiny 2'
        elif self.game == 5:
            game = 'Counter - Strike: Global Offensive'
        elif self.game == 6:
            game = "PlayerUnknown's BATTLEGROUNDS"
        elif self.game == 7:
            game = 'Rainbow Six Siege'
        elif self.game == 8:
            game = 'Overwatch'
        elif self.game == 9:
            game = 'League of Legends'
        elif self.game == 10:
            game = 'Hearthstone'
        elif self.game == 11:
            game = 'World of Warcraft'
        elif self.game == 12:
            game = 'SMITE'
        elif self.game == 13:
            game = 'Rocket League'
        elif self.game == 14:
            game = 'Battlefield 1'

        return format + " " + platform + " " + game + " " + str(self.start)

    def set_inactive(self, **kwargs):
        pk = self.kwargs['pk']
        tournament = SingleEliminationTournament.objects.get(id=pk)
        tournament.active = False
        tournament.save()

    def generate_rounds(self):
        # create the round objects based on the tournament size
        if self.size == 4:
            # generate 2 rounds
            round1 = SingleTournamentRound(matchesnum=2, roundnum=1, tournament=self)
            round1.save()
            round2 = SingleTournamentRound(matchesnum=1, roundnum=2, tournament=self)
            round2.save()
        elif self.size == 8:
            # generate 3 rounds
            round1 = SingleTournamentRound(matchesnum=4, roundnum=1, tournament=self)
            round2 = SingleTournamentRound(matchesnum=2, roundnum=2, tournament=self)
            round3 = SingleTournamentRound(matchesnum=1, roundnum=3, tournament=self)
            round1.save()
            round2.save()
            round3.save()
        elif self.size == 16:
            # generate 4 rounds
            round1 = SingleTournamentRound(matchesnum=8, roundnum=1, tournament=self)
            round2 = SingleTournamentRound(matchesnum=4, roundnum=2, tournament=self)
            round3 = SingleTournamentRound(matchesnum=2, roundnum=3, tournament=self)
            round4 = SingleTournamentRound(matchesnum=1, roundnum=4, tournament=self)
            round1.save()
            round2.save()
            round3.save()
            round4.save()
        elif self.size == 32:
            # generate 5 rounds
            round1 = SingleTournamentRound(matchesnum=16, roundnum=1, tournament=self)
            round2 = SingleTournamentRound(matchesnum=8, roundnum=2, tournament=self)
            round3 = SingleTournamentRound(matchesnum=4, roundnum=3, tournament=self)
            round4 = SingleTournamentRound(matchesnum=2, roundnum=4, tournament=self)
            round5 = SingleTournamentRound(matchesnum=1, roundnum=5, tournament=self)
            round1.save()
            round2.save()
            round3.save()
            round4.save()
            round5.save()
        elif self.size == 64:
            # generate 6 rounds
            pass
        elif self.size == 128:
            # generate 7 rounds
            pass

    def generate_bracket(self, **kwargs):
        # seed teams and make matches
        pk = self.kwargs['pk']
        tournament = SingleEliminationTournament.objects.get(id=pk)
        game = tournament.game
        platform = tournament.platform
        teamformat = tournament.teamformat
        bestof = tournament.bestof
        size = tournament.size
        numteams = tournament.teams.count
        bye = size - numteams
        if size == 4:
            # 1 play 4
            # 2 plays 3
            # 2 matches need to be played in round 1
            # 1 match needs to be played in round 2
            # total number of rounds = 2
            round1 = SingleTournamentRound.objects.get(roundnum=1, tournament=tournament)
            rounds = 2
            round1matches = 2
            round2matches = 1
            bracketsize = 4
            seeds = [1, 2, 3, 4]
            possible_seeds = [1, 2, 3, 4]
            for i in numteams:
                team = Team.objects.get(id=pk)
                tournament_team = SingleTournamentTeam.objects.get(id=pk)
                randseed = (random.choice(seeds))
                possible_seeds.pop(randseed - 1)
                tournament_team.seed = randseed
                tournament_team.save()

                if tournament_team.seed == 1:
                    # they are seeded first they play 4th seeded team
                    match1 = Match(game=game, platform=platform, hometeam=tournament_team, teamformat=teamformat,
                                   bestof=bestof)
                    round1 = SingleTournamentRound.objects.get(tournament=tournament, roundnum=1)
                    round1.add(matches=match1)
                    round1.save()
                    match1.save()
                elif tournament_team.seed == 2:
                    # hey you play in match2 against seed 3
                    match2 = Match(game=game, platform=platform, hometeam=tournament_team, teamformat=teamformat,
                                   bestof=bestof)
                    round1 = SingleTournamentRound.objects.get(tournament=tournament, roundnum=1)
                    round1.add(matches=match2)
                    round1.save()
                    match2.save()
                elif tournament_team.seed == 3:
                    match2 = Match(game=game, platform=platform, awayteam=tournament_team, teamformat=teamformat,
                                   bestof=bestof)
                    round1 = SingleTournamentRound.objects.get(tournament=tournament, roundnum=1)
                    round1.add(matches=match2)
                    round1.save()
                    match2.save()
                elif tournament_team.seed == 4:
                    match1 = Match(game=game, platform=platform, awayteam=tournament_team, teamformat=teamformat,
                                   bestof=bestof)
                    round1 = SingleTournamentRound.objects.get(tournament=tournament, roundnum=1)
                    round1.add(matches=match1)
                    round1.save()
                    match1.save()

        elif size == 8:
            # 1 plays 8
            # 2 plays 7
            # 3 plays 6
            # 4 plays 5
            # 4 matches need to be played in round 1
            # total number of rounds = 3
            rounds = 3
            actual_teams = numteams
            bracketsize = 8
            seeds = [1,2,3,4,5,6,7,8]
            possible_seeds = [1,2,3,4,5,6,7,8]
            for i in numteams:
                team = Team.objects.get(id=pk)
                tournament_team = SingleTournamentTeam.objects.get(id=pk)
                randseed = (random.choice(seeds))
                possible_seeds.pop(randseed - 1)
                tournament_team.seed = randseed
                tournament_team.save()

                if tournament_team.seed == 1:
                    # they are seeded first they play 4th seeded team
                    match1 = Match(game=game, platform=platform, hometeam=tournament_team, teamformat=teamformat,
                                   bestof=bestof)
                    round1 = SingleTournamentRound.objects.get(tournament=tournament, roundnum=1)
                    round1.add(matches=match1)
                    round1.save()
                    match1.save()
                elif tournament_team.seed == 2:
                    # hey you play in match2 against seed 3
                    match2 = Match(game=game, platform=platform, hometeam=tournament_team, teamformat=teamformat,
                                   bestof=bestof)
                    round1 = SingleTournamentRound.objects.get(tournament=tournament, roundnum=1)
                    round1.add(matches=match2)
                    round1.save()
                    match2.save()
                elif tournament_team.seed == 3:
                    match3 = Match(game=game, platform=platform, awayteam=tournament_team, teamformat=teamformat,
                                   bestof=bestof)
                    round1 = SingleTournamentRound.objects.get(tournament=tournament, roundnum=1)
                    round1.add(matches=match3)
                    round1.save()
                    match3.save()
                elif tournament_team.seed == 4:
                    match4 = Match(game=game, platform=platform, awayteam=tournament_team, teamformat=teamformat,
                                   bestof=bestof)
                    round1 = SingleTournamentRound.objects.get(tournament=tournament, roundnum=1)
                    round1.add(matches=match4)
                    round1.save()
                    match4.save()

                elif tournament_team.seed == 5:
                    match4 = Match(game=game, platform=platform, awayteam=tournament_team, teamformat=teamformat,
                                   bestof=bestof)
                    round1 = SingleTournamentRound.objects.get(tournament=tournament, roundnum=1)
                    round1.add(matches=match4)
                    round1.save()
                    match4.save()

                elif tournament_team.seed == 6:
                    match3 = Match(game=game, platform=platform, awayteam=tournament_team, teamformat=teamformat,
                                   bestof=bestof)
                    round1 = SingleTournamentRound.objects.get(tournament=tournament, roundnum=1)
                    round1.add(matches=match3)
                    round1.save()
                    match3.save()

                elif tournament_team.seed == 7:
                    match2 = Match(game=game, platform=platform, awayteam=tournament_team, teamformat=teamformat,
                                   bestof=bestof)
                    round1 = SingleTournamentRound.objects.get(tournament=tournament, roundnum=1)
                    round1.add(matches=match2)
                    round1.save()
                    match2.save()

                elif tournament_team.seed == 8:
                    match1 = Match(game=game, platform=platform, awayteam=tournament_team, teamformat=teamformat,
                                   bestof=bestof)
                    round1 = SingleTournamentRound.objects.get(tournament=tournament, roundnum=1)
                    round1.add(matches=match1)
                    round1.save()
                    match1.save()

        elif size == 16:
            # 1 plays 16
            # 2 plays 15
            # 3 plays 14
            # 4 plays 13
            # 5 plays 12
            # and so on
            # 8 matches need to be played in round 1
            # total number of rounds = 4
            rounds = 4
            actual_teams = numteams
            bracketsize = 16

            pass
        elif size == 32:
            # 1 plays 32
            # 2 plays 31
            # and so on
            # 16 matches need to be played in round 1
            # 8 round 2
            # 4 round 3
            # 2 round 4
            # 1 round 5 (winners match)
            # total number of rounds = 5
            rounds = 5
            actual_teams = numteams
            bracketsize = 32

            pass
        elif size == 64:
            # the same thing
            # 32 matches need to be played in round 1
            # 16 round 2
            # 8 round 3
            # 4 round 4
            # 2 round 5
            # 1 round 6 (winners match)
            # total number of rounds = 6
            rounds = 6
            actual_teams = numteams
            bracketsize = 64

            pass
        elif size == 128:
            # same thing
            # 64 matches need to be played in round 1
            # 32 round 2
            # 16 round 3
            # 8 round 4
            # 4 round 5
            # 2 round 6
            # 1 round 7
            # total number of rounds = 7
            rounds = 7
            actual_teams = numteams
            bracketsize = 128

            pass

    def rounds_required(self):
        if self.size == 4:
            return 2
        elif self.size == 8:
            return 3
        elif self.size == 16:
            return 4
        elif self.size == 32:
            return 5
        elif self.size == 64:
            return 6
        elif self.size == 128:
            return 7
        else:
            # something got fucked up
            return 0

    def get_round1_byes(self, **kwargs):
        # only used for round 1 purposes
        pk = self.kwargs['pk']
        tournament = SingleEliminationTournament.objects.get(id=pk)
        return tournament.size - tournament.teams.count

    def get_num_teams(self):
        return self.teams.count


class SingleTournamentRound(models.Model):
    # ManyToManyField to keep track of the teams that are still active and have matches to play in the round
    teams = models.ManyToManyField(Team)

    # what round number is this? round 1 is the first round of the tournament
    roundnum = models.PositiveSmallIntegerField(default=1)

    # how many matches will be played in this round? Set the default to the minimum
    matchesnum = models.PositiveSmallIntegerField(default=2)

    tournament = models.ForeignKey(SingleEliminationTournament, related_name='withtournamentround',
                                   on_delete=models.CASCADE)

    # ManyToMany Field to keep track of the matches that were assigned and created for this given round...
    matches = models.ManyToManyField(Match)


class SingleTournamentTeam(models.Model):
    team = models.ForeignKey(Team, related_name='actualteam', null=True, on_delete=models.CASCADE)
    round = models.ForeignKey(SingleTournamentRound, related_name='teaminround', null=True, on_delete=models.CASCADE)
    seed = models.PositiveIntegerField(default=0)
    tournament = models.ForeignKey(SingleEliminationTournament, related_name='intournament', null=True,
                                   on_delete=models.CASCADE)
