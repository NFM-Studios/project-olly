import random

from django.db import models

from matches.models import Match, GameChoice, PlatformChoice, MapPoolChoice, MapChoice, SportChoice
from matches.settings import TEAMFORMAT_CHOICES, MAPFORMAT_CHOICES
from profiles.models import User
from teams.models import Team

SIZE_CHOICES = (
    (4, 4),
    (8, 8),
    (16, 16),
    (32, 32),
    (64, 64),
    (128, 128),
)


class SingleTournamentRuleset(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    text = models.TextField()
    creator = models.ForeignKey(User, related_name='rulesetCreator', on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class SingleEliminationTournament(models.Model):
    name = models.CharField(max_length=50, blank=False, default='No name provided', unique=True)
    # I know we need the team format, ex 1v1, 2v2, 3v3, 4v4, 5v5, 6v6
    teamformat = models.SmallIntegerField(choices=TEAMFORMAT_CHOICES, default=1)
    # by default its a best of 1. Not sure if we need this here. Finals might be best of 3, etc in
    # the future possibly. TBD. For now this will work though.
    bestof = models.SmallIntegerField(choices=MAPFORMAT_CHOICES, default=0)

    # by default the tournament is not active. an admin has to activate it in order for it to be public
    active = models.BooleanField(default=False)

    # custom olly - twitch tourament
    twitch = models.CharField(max_length=60, default='twitch')

    # when does registration open, and when does it close? specified when created in staff panel
    open_register = models.DateTimeField()
    # dont allow people to join once registration is closed
    close_register = models.DateTimeField()

    # temp fix for registration since timezones are being a bitch
    allow_register = models.BooleanField(default=False)

    # general information about the tournament
    info = models.TextField(default="No information provided")

    ruleset = models.ForeignKey(SingleTournamentRuleset, related_name='tournamentruleset', on_delete=models.PROTECT,
                                null=True)

    # the time the specific tournament object was created
    created = models.DateTimeField(auto_now_add=True)
    # last time an admin updated something
    updated = models.DateTimeField(auto_now=True)

    req_credits = models.PositiveSmallIntegerField(default=0)

    # game and platform it will be played on
    platform = models.ForeignKey(PlatformChoice, on_delete=models.PROTECT, null=True, blank=True)
    game = models.ForeignKey(GameChoice, related_name='game', on_delete=models.PROTECT, null=True, blank=True)

    sport = models.ForeignKey(SportChoice, related_name='sport', on_delete=models.PROTECT, null=True, blank=True)

    # when will the first round of matches start?
    start = models.DateTimeField()

    # all the teams that are in the event. eligibility happens inside the view, when they try to register @ben told me
    #  how to do this mtm field, i forgot
    teams = models.ManyToManyField(Team, blank=True)

    current_round = models.SmallIntegerField(default=1, blank=True)

    # specify the winning team when they are declared
    winner = models.ForeignKey(Team, related_name='winningteam', on_delete=models.SET_NULL, blank=True, null=True)

    # specify second place, just for storage and future reference
    second = models.ForeignKey(Team, related_name='secondplaceteam', on_delete=models.SET_NULL, blank=True, null=True)

    third = models.ForeignKey(Team, related_name='thirdplaceteam', on_delete=models.SET_NULL, blank=True, null=True)

    # specify how many teams the event will be capped at, and the size of the bracket
    size = models.PositiveSmallIntegerField(default=32, choices=SIZE_CHOICES)

    xp_seed = models.BooleanField(default=False)

    bracket_generated = models.BooleanField(default=False)

    map_pool = models.ForeignKey(MapPoolChoice, related_name='map_pool', on_delete=models.SET_NULL, null=True)

    # the prizes that they will win, defined in admin panel. 3rd place isnt really needed..... just first and second...
    prize1 = models.CharField(default='no prize specified', max_length=50)
    prize2 = models.CharField(default='no prize specified', max_length=50)
    prize3 = models.CharField(default='no prize specified', max_length=50)

    image = models.ImageField(upload_to='tournament_images', blank=True)

    # if set to true, admins will have manually input the result of each match, users will not be able to report wins
    # when matches are created it will set the match field to whatever this field is set to.
    disable_userreport = models.BooleanField(default=True)

    # need to figure out how we will work rules rules = models.ForeignKey(Ruleset, related_name='tournamentrules',
    # on_delete=models.CASCADE, blank=False, null=True)

    def __str__(self):
        return self.name  # + self.platform + self.game

    def generate_maps(self, roundpk):
        pool = self.map_pool
        poolsize = pool.maps.count()
        try:
            round = SingleTournamentRound.objects.get(id=roundpk)
        except:
            return False
        if round:
            matches = round.matches
            for match in matches:
                mike = random.random(1, poolsize)
                temp_map = MapChoice.objects.get(map_num=mike)
                match.map = temp_map

    def set_inactive(self, **kwargs):
        pk = self.kwargs['pk']
        tournament = SingleEliminationTournament.objects.get(id=pk)
        tournament.active = False
        tournament.save()

    def generate_bracket(self):
        teams = len(self.teams.all())
        myteams = self.teams.all()
        round1 = SingleTournamentRound(tournament=self)
        if teams % 2 == 0:
            # no byes required - get 2 teams and make a match
            while len(myteams) != 0:
                temp1 = myteams.all().order_by("?").first()
                temp2 = myteams.all().order_by("?").first()
                tempmatch = Match(awayteam=temp1, hometeam=temp2, maps=self.map_pool, game=self.game, platform=self.platform)
                tempmatch.save()
                myteams.remove(temp1)
                myteams.remove(temp2)
                round1.matches.add(tempmatch)

        else:
            # take the first team and give them a bye
            # TODO: verify this randomly grabs a random team
            bteam = self.teams.all.order_by("?").first()
            bmatch = Match(hometeam=None, bye_1=True, awayteam=bteam, winner=bteam, completed=True,
                           type='singletournament', maps=self.map_pool, game=self.game, platform=self.platform)
            bmatch.save()
            round1.matches.add(bmatch)
            myteams.remove(bteam)
            if len(myteams) % 2 != 0:
                print("ITS BROKEN YOU SUCK")
                return
            while len(myteams) != 0:
                temp1 = myteams.all().order_by("?").first()
                temp2 = myteams.all().order_by("?").first()
                tempmatch = Match(awayteam=temp1, hometeam=temp2, maps=self.map_pool, game=self.game, platform=self.platform)
                tempmatch.save()
                myteams.remove(temp1)
                myteams.remove(temp2)
                round1.matches.add(tempmatch)

        round1.save()

    def get_round1_byes(self, **kwargs):
        # only used for round 1 purposes
        pk = self.kwargs['pk']
        tournament = SingleEliminationTournament.objects.get(id=pk)
        return tournament.size - tournament.teams.count

    def get_num_teams(self):
        return self.teams.count


class SingleTournamentRound(models.Model):
    # ManyToManyField to keep track of the teams that are still active and have matches to play in the round
    # teams = models.ManyToManyField(Team)

    # what round number is this? round 1 is the first round of the tournament
    roundnum = models.PositiveSmallIntegerField(default=1)

    # how many matches will be played in this round? Set the default to the minimum
    matchesnum = models.PositiveSmallIntegerField(default=2)

    tournament = models.ForeignKey(SingleEliminationTournament, related_name='withtournamentround',
                                   on_delete=models.CASCADE)

    # ManyToMany Field to keep track of the matches that were assigned and created for this given round...
    matches = models.ManyToManyField(Match)

    info = models.TextField(default='No info specified')


class SingleTournamentTeam(models.Model):
    team = models.ForeignKey(Team, related_name='actualteam', null=True, on_delete=models.CASCADE)
    seed = models.PositiveIntegerField(default=0, null=True, blank=True)
    tournament = models.ForeignKey(SingleEliminationTournament, related_name='intournament', null=True,
                                   on_delete=models.CASCADE)
