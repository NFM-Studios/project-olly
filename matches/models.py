from django.contrib.auth.models import User
from django.db import models
from matches.settings import TEAMFORMAT_CHOICES, MAPFORMAT_CHOICES
from teams.models import Team


class StatsPlayer(models.Model):
    rating = models.DecimalField(max_digits=6, decimal_places=3, default=0)
    kills = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)
    deaths = models.IntegerField(default=0)
    killround = models.DecimalField(max_digits=6, decimal_places=3, default=0)
    adr = models.IntegerField(default=0)
    ud = models.IntegerField(default=0)
    ef = models.IntegerField(default=0)
    f_assists = models.IntegerField(default=0)
    hs = models.IntegerField(default=0)
    kast = models.IntegerField(default=0)
    awp_k = models.IntegerField(default=0)
    twok = models.IntegerField(default=0)
    threek = models.IntegerField(default=0)
    fourk = models.IntegerField(default=0)
    fivek = models.IntegerField(default=0)
    one_v_one = models.IntegerField(default=0)
    one_v_two = models.IntegerField(default=0)
    one_v_three = models.IntegerField(default=0)
    one_v_four = models.IntegerField(default=0)
    one_v_five = models.IntegerField(default=0)
    f_kills = models.IntegerField(default=0)
    f_deaths = models.IntegerField(default=0)
    entries = models.IntegerField(default=0)
    trades = models.IntegerField(default=0)
    rounds = models.IntegerField(default=0)
    rf = models.IntegerField(default=0)
    ra = models.IntegerField(default=0)
    damage = models.IntegerField(default=0)


class TeamMatchStats(models.Model):
    rounds_won = models.PositiveSmallIntegerField(default=0)
    rounds_lost = models.PositiveSmallIntegerField(default=0)
    total_kills = models.PositiveSmallIntegerField(default=0)
    total_deaths = models.PositiveSmallIntegerField(default=0)
    avg_rating = models.DecimalField(max_digits=6, decimal_places=3, default=0)
    avg_killround = models.DecimalField(max_digits=6, decimal_places=3, default=0)
    avg_adr = models.IntegerField(default=0)
    avg_ud = models.IntegerField(default=0)
    avg_ef = models.IntegerField(default=0)
    total_rating = models.DecimalField(max_digits=6, decimal_places=3, default=0)
    total_killround = models.DecimalField(max_digits=6, decimal_places=3, default=0)
    total_adr = models.IntegerField(default=0)
    total_ud = models.IntegerField(default=0)
    total_ef = models.IntegerField(default=0)
    # ??? f_assists = models.IntegerField(default=0)
    avg_hs = models.IntegerField(default=0)
    avg_kast = models.IntegerField(default=0)
    awp_k = models.IntegerField(default=0)
    twok = models.IntegerField(default=0)
    threek = models.IntegerField(default=0)
    fourk = models.IntegerField(default=0)
    fivek = models.IntegerField(default=0)
    one_v_one = models.IntegerField(default=0)
    one_v_two = models.IntegerField(default=0)
    one_v_three = models.IntegerField(default=0)
    one_v_four = models.IntegerField(default=0)
    one_v_five = models.IntegerField(default=0)
    f_kills = models.IntegerField(default=0)
    f_deaths = models.IntegerField(default=0)
    entries = models.IntegerField(default=0)
    trades = models.IntegerField(default=0)
    # rounds played
    rounds = models.IntegerField(default=0)
    avg_damage = models.IntegerField(default=0)
    total_damage = models.IntegerField(default=0)


class MatchStats(models.Model):
    matchid = models.PositiveIntegerField(default=0)
    map = models.CharField(default="unknown", max_length=255)
    team1 = models.CharField(default="unknown", max_length=255)
    team2 = models.CharField(default="unknown", max_length=255)


class SportChoice(models.Model):
    name = models.CharField(default='unknown sports', null=False, max_length=255)

    def __str__(self):
        return "" + self.name


class GameChoice(models.Model):
    name = models.CharField(default='unknown', null=False, max_length=255)
    image = models.ImageField(upload_to='game_images', blank=True)

    def __unicode__(self):
        return '%s' % self.name

    def __str__(self):
        return "" + self.name


class PlatformChoice(models.Model):
    name = models.CharField(default='unknown', null=False, max_length=255)
    image = models.ImageField(upload_to='platform_images', null=True, blank=True)

    def __unicode__(self):
        return "" + self.name

    def __str__(self):
        return "" + self.name


all_games = GameChoice.objects.all()
all_platforms = PlatformChoice.objects.all()


class MapChoice(models.Model):
    name = models.CharField(default='default_map', null=False, max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    map_num = models.IntegerField(default=0, null=True, blank=True)
    game = models.ForeignKey(GameChoice, related_name='map_for', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class MapPoolChoice(models.Model):
    name = models.CharField(default='default map pool', null=False, max_length=255)
    maps = models.ManyToManyField(MapChoice, blank=True)
    description = models.CharField(default="No map pool description", max_length=255)
    game = models.ForeignKey(GameChoice, related_name='map_pool_for', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # def add_map(self, mappk):
    #    newmap = MapChoice.objects.get(id=mappk)
    #    newmap.map_num = self.maps.count() + 1
    #    self.maps.add(newmap)

    def __str__(self):
        return self.name


class Match(models.Model):
    type = models.CharField(blank=True, null=True, max_length=20)
    matchnum = models.SmallIntegerField(default=0)
    map_pool = models.ForeignKey(MapPoolChoice, related_name='mappoolchoice', on_delete=models.SET_NULL, null=True)
    maps = models.ManyToManyField(MapChoice, blank=True)
    game = models.ForeignKey(GameChoice, related_name='GameChoice', on_delete=models.PROTECT, null=True)
    # default to ps4 for now bc why not
    platform = models.ForeignKey(PlatformChoice, related_name='PlatformChoice', on_delete=models.PROTECT, null=True)
    # support for traditional sports
    sport = models.ForeignKey(SportChoice, related_name='SportChoice', on_delete=models.PROTECT, null=True, blank=True)
    # assign the match to a tournament with a FK
    # tournament = models.ForeignKey(SingleEliminationTournament, related_name='tournament', on_delete=models.CASCADE)
    # fk fields for the 2 teams that are competiting,
    # verification for elgible teams happens within the tournament and teams app
    # home team is team 1
    hometeam = models.ForeignKey(Team, related_name='hometeam', on_delete=models.SET_NULL, null=True)
    # away team is team 2
    awayteam = models.ForeignKey(Team, related_name='awayteam', on_delete=models.SET_NULL, null=True)
    # simple bool field to see if the match scores have been reported
    reported = models.BooleanField(default=False)
    # simple bool field to see if the entire match is completed
    completed = models.BooleanField(default=False)
    config_generated = models.BooleanField(default=False)
    # field to declare the winner
    winner = models.ForeignKey(Team, related_name='champions', on_delete=models.SET_NULL, null=True, blank=True)
    loser = models.ForeignKey(Team, related_name='loser', on_delete=models.SET_NULL, null=True, blank=True)
    # set the default map format to best of 1
    bestof = models.SmallIntegerField(choices=MAPFORMAT_CHOICES, default=1)
    #          by default set it to be a 2v2.
    teamformat = models.SmallIntegerField(choices=TEAMFORMAT_CHOICES, default=1)

    team1reported = models.BooleanField(default=False)
    team1reportedwinner = models.ForeignKey(Team, related_name='team1reportedwinner', on_delete=models.SET_NULL,
                                            null=True, blank=True)
    team2reported = models.BooleanField(default=False)
    team2reportedwinner = models.ForeignKey(Team, related_name='team2reportedwinner', on_delete=models.SET_NULL,
                                            null=True, blank=True)

    server = models.CharField(blank=True, null=True, max_length=255)

    datetime = models.DateTimeField(null=True, blank=True)

    info = models.TextField(default="Match Info: ")

    disputed = models.BooleanField(default=False)

    bye_1 = models.BooleanField(default=False)

    bye_2 = models.BooleanField(default=False)
    # if set to true, admins will have manually input the result of each match, users will not be able to report wins
    disable_userreport = models.BooleanField(default=True)
    # is the match played between two teams in the same conference (mostly for leagues)
    conference_match = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "matches"

    def update_info(self, obj):
        self.info = obj.info
        self.save()

    def get_min_team_size(self):
        if self.teamformat == 0:
            return 1
        if self.teamformat == 1:
            return 2
        if self.teamformat == 2:
            return 3
        if self.teamformat == 3:
            return 4
        if self.teamformat == 4:
            return 5
        if self.teamformat == 5:
            return 6


class MatchCheckIn(models.Model):
    match = models.ForeignKey(Match, related_name='match_checkin', on_delete=models.SET_NULL, null=True)
    reporter = models.ForeignKey(User, related_name='checkin_user', on_delete=models.SET_NULL, null=True)
    team = models.ForeignKey(Team, related_name='checking_in_team', on_delete=models.SET_NULL, null=True)
    # players should == match.get_min_team_size
    players = models.ManyToManyField(User)


class MatchReport(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    # see the time the report was made for admins
    match = models.ForeignKey(Match, related_name='matchreporting', on_delete=models.CASCADE)
    reporting_team = models.ForeignKey(Team, related_name='teamreporting', on_delete=models.SET_NULL, null=True)
    reporting_user = models.ForeignKey(User, related_name='userreporting', on_delete=models.SET_NULL, null=True)
    # who the person reporting is declaring the winner as
    reported_winner = models.ForeignKey(Team, related_name='winnerreporting', on_delete=models.SET_NULL, null=True)
    proof = models.CharField(max_length=300, default='no text inserted', blank=False)


class MatchDispute(models.Model):
    # save when it  was created and last  updated
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # save the 2 teams that are  involved in the match,  and thus involved in this dispute
    # team1 should line up to team1 of the original match, and same for team2.
    team1 = models.ForeignKey(Team, related_name='team1', on_delete=models.SET_NULL, null=True)
    team2 = models.ForeignKey(Team, related_name='team2', on_delete=models.SET_NULL, null=True)

    # the match object that is currently being disputed
    match = models.ForeignKey(Match, related_name='disputedMatch', on_delete=models.CASCADE)

    # proof  that each team submits to an admin
    # teamproof = models.CharField(max_length=300, default='(team 1) no text inserted', blank=False)
    teamproof_1 = models.URLField(blank=False)
    teamproof_2 = models.URLField(blank=True)
    teamproof_3 = models.URLField(blank=True)
    # who submitted the original match report, hence causing this dispute
    team1origreporter = models.ForeignKey(User, related_name='team1OriginalReporter',
                                          on_delete=models.SET_NULL, null=True)
    team2origreporter = models.ForeignKey(User, related_name='team2OriginalReporter',
                                          on_delete=models.SET_NULL, null=True)

    # who is submitting the proof for the dispute
    teamreporter = models.ForeignKey(User, related_name='team1Disputer', on_delete=models.SET_NULL, null=True,
                                     blank=True)

    # once all this information is submitted it will be viewable  by an admin that will look at the proof and
    # determine who the winner is.
