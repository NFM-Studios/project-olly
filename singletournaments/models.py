from django.db import models
from matches.settings import GAME_CHOICES, PLATFORMS_CHOICES, TEAMFORMAT_CHOICES, MAPFORMAT_CHOICES
from matches.models import Ruleset, Match
from teams.models import Team
from random import *

SIZE_CHOICES = (
    (4,4),
    (8,8),
    (16,16),
    (32,32),
    (64,64),
    (128,128),
)




class SingleEliminationTournament(models.Model):

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
    teams = models.ManyToManyField(Team)


    # specify the winning team when they are declared
    winner = models.ForeignKey(Team, related_name='winningteam', on_delete=models.CASCADE)

    # specify second place, just for storage and future reference
    second = models.ForeignKey(Team, related_name='secondplaceteam', on_delete=models.CASCADE)


    # specify how many teams the event will be capped at, and the size of the bracket
    size = models.PositiveSmallIntegerField(default=32, choices=SIZE_CHOICES)

    # the prizes that they will win, defined in admin panel. 3rd place isnt really needed..... just first and second...
    prize1 = models.CharField(default='no prize specified', max_length=50)
    prize2 = models.CharField(default='no prize specified', max_length=50)
    prize3 = models.CharField(default='no prize specified', max_length=50)

    # need to figure out how we will work rules
    rules = models.ForeignKey(Ruleset, related_name='tournamentrules', on_delete=models.CASCADE)

    def __str__(self):
        return (teamformat + " " + platform + " " + game + " " + start)

    def __init__(self):
        tournament = SingleEliminationTournament.get(id=pk)
        size = tournament.size
        teams = tournament.teams
        if size == 4:
            # generate 2 rounds
            round1 = SingleTournamentRound(matchesnum=2, roundnum=1, tournament=tournament, teams=teams)
            round1.save()
            round2 = SingleTournamentRound(matchesnum=1, roundnum=2, tournament=tournament)
            round2.save()
        elif size == 8:
            # generate 3 rounds
            pass
        elif size == 16:
            # generate 4 rounds
            pass
        elif size == 32:
            # generate 5 rounds
            pass
        elif size == 64:
            # generate 6 rounds
            pass
        elif size == 128:
            # generate 7 rounds
            pass

    def generate_bracket(self):
        tournament = SingleEliminationTournament.get(id=pk)
        size = tournament.size
        numteams = tournament.teams.count
        bye = size - numteams
        if size == 4:
            # 1 play 4
            # 2 plays 3
            # 2 matches need to be played in round 1
            # 1 match needs to be played in round 2
            # total number of rounds = 2
            round1 = SingleTournamentRound.get(id=pk)
            rounds = 2
            round1matches = 2
            round2matches = 1
            bracketsize = 4
            seeds = [1,2,3,4]
            possible_seeds = [1, 2, 3, 4]
            for i in numteams:
                team = Team.get(id=pk)
                tournament_team = SingleTournamentTeam.get(id=pk)
                randseed = (random.choice(seeds))
                possible_seeds.pop(randseed-1)
                tournament_team.seed = randseed
                tournament_team.save()


            pass
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

            pass
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
            actual_teams =  numteams
            bracketsize = 128

            pass

    def generate_matches(self):
        # a
        pass
    def rounds_required(self):
        # the number of rounds required
        # teams/2
        pass

class SingleTournamentRound(models.Model):
    # ManyToManyField to keep track of the teams that are still active and have matches to play in the round
    teams = models.ManyToManyField(Team)

    # what round number is this? round 1 is the first round of the tournament
    roundnum = models.PositiveSmallIntegerField(default=1)

    # how many matches will be played in this round? Set the default to the minimum
    matchesnum = models.PositiveSmallIntegerField(default=2)

    tournament = models.ForeignKey(SingleEliminationTournament, related_name='withtournamentround', on_delete=models.CASCADE)

    # ManyToMany Field to keep track of the matches that were assigned and created for this given round...
    matches = models.ManyToManyField(Match)

class SingleTournamentTeam(models.Model):
    team = models.ForeignKey(Team, related_name='actualteam', null=True, on_delete=models.CASCADE)
    round = models.ForeignKey(SingleTournamentRound, related_name='teaminround', null=True, on_delete=models.CASCADE)
    seed = models.PositiveIntegerField(default=0)
    tournament = models.ForeignKey(SingleEliminationTournament, related_name='intournament', null=True, on_delete=models.CASCADE)