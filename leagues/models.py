from django.db import models
from teams.models import Team
from matches.models import Match, GameChoice, PlatformChoice, MapPoolChoice, MapChoice, SportChoice
from matches.settings import TEAMFORMAT_CHOICES, MAPFORMAT_CHOICES
from singletournaments.models import SingleTournamentRuleset
from profiles.models import UserProfile


# a way to create default values for a field over multiple seasons
class LeagueSettings(models.Model):
    name = models.CharField(default='League Ruleset', max_length=50)
    # whether or not to keep track of Overtime Losses in a separate column
    ot_losses = models.BooleanField(default=True)
    # amount of points to award a team for an overtime loss
    pts_ot_loss = models.PositiveSmallIntegerField(default=1)
    # whether or not to keep track of Overtime wins in a separate column
    ot_wins = models.BooleanField(default=False)
    pts_ot_win = models.PositiveSmallIntegerField(default=3)
    # amount of points to award teams for a win
    pts_win = models.PositiveSmallIntegerField(default=3)
    pts_loss = models.PositiveSmallIntegerField(default=0)
    # whether or not to allow tie
    allow_tie = models.BooleanField(default=False)
    # number of games each team plays during the regular season
    num_games = models.PositiveIntegerField(default=10)
    # automatically schedule games. TODO - implement auto schedule
    auto_schedule = models.BooleanField(default=False)
    # automatically generate matches, enabling this will create matches but will not set match times
    auto_matchup = models.BooleanField(default=False)
    # W=Win, L=Loss, OTL=Overtime Loss, T=Tie, OTW=Overtime Win, OTT=Overtime Tie
    RECORD_FORMAT_CHOICES = (
        (1, "W-L-OTL"),
        (2, "W-L-T"),
        (3, "W-L-OTW-OTL"),
        (4, "W-L-OTW-OTL-OTT"),
        (5, "W-L"),
    )
    # record format to show on front end
    # record_format = models.CharField(choices=RECORD_FORMAT_CHOICES, default=1, max_length=20)
    # number of divisions to break teams into
    num_divisions = models.PositiveSmallIntegerField(default=2)
    # max amount of teams to allow into a division
    max_division_size = models.PositiveSmallIntegerField(default=5)
    # is xbl required to join?
    require_xbl = models.BooleanField(default=False)
    require_psn = models.BooleanField(default=False)
    require_steam = models.BooleanField(default=False)
    require_epic = models.BooleanField(default=False)
    require_lol = models.BooleanField(default=False)
    require_battlenet = models.BooleanField(default=False)
    require_activision = models.BooleanField(default=False)
    # whether or not to allow users to register as a free agent to the league
    allow_fa = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class LeagueTeam(models.Model):
    class Meta:
        ordering = ['-points']
    team = models.ForeignKey(Team, related_name='league_team', on_delete=models.PROTECT)
    wins = models.PositiveSmallIntegerField(default=0)
    losses = models.PositiveSmallIntegerField(default=0)
    ot_losses = models.PositiveSmallIntegerField(default=0)
    ot_wins = models.PositiveSmallIntegerField(default=0)
    ties = models.PositiveSmallIntegerField(default=0)
    points = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.team.name


class LeagueDivision(models.Model):
    # name for the league division - set to null in case admins wish to manually change it
    name = models.CharField(null=True, max_length=50)
    # teams that are in that division, allow it to be empty
    teams = models.ManyToManyField(LeagueTeam, blank=True)
    # games that are to be played and have been played in that division, blank until all matches are generated
    matches = models.ManyToManyField(Match, blank=True)

    def __str__(self):
        if self.name is None:
            return "Division "+str(self.pk)
        else:
            return self.name


class LeagueFreeAgent(models.Model):
    user = models.ForeignKey(UserProfile, related_name='fa_profile', on_delete=models.CASCADE)
    description = models.TextField(default="Include information about Free Agent here")


class League(models.Model):
    LEAGUE_STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('preseason', 'Preseason'),
        ('regular season', 'Regular Season'),
        ('playoffs', 'Playoffs'),
        ('finals', 'Finals'),
        ('offseason', 'Offseason'),
    )
    name = models.CharField(default="League Name", max_length=50)
    status = models.CharField(choices=LEAGUE_STATUS_CHOICES, max_length=50, default='preseason')
    settings = models.ForeignKey(LeagueSettings, related_name="league_settings", on_delete=models.PROTECT)
    ruleset = models.ForeignKey(SingleTournamentRuleset, related_name="league_ruleset", on_delete=models.PROTECT)
    # if set to true the league will display on the front page, false and it will not
    active = models.BooleanField(default=False)
    info = models.TextField(default="No information provided")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    divisions = models.ManyToManyField(LeagueDivision, blank=True)
    platform = models.ForeignKey(PlatformChoice, related_name='league_platform', on_delete=models.PROTECT, null=True, blank=True)
    game = models.ForeignKey(GameChoice, related_name='league_game', on_delete=models.PROTECT, null=True, blank=True)
    sport = models.ForeignKey(SportChoice, related_name='league_sport', on_delete=models.PROTECT, null=True, blank=True)
    image = models.ImageField(upload_to='league_images', blank=True, null=True)
    # team format, ex 1v1, 2v2, 3v3, 4v4, 5v5, 6v6
    teamformat = models.SmallIntegerField(choices=TEAMFORMAT_CHOICES, default=1)
    # by default its a best of 1. Not sure if we need this here. Finals might be best of 3, etc in
    # the future possibly. TBD. For now this will work though.
    bestof = models.SmallIntegerField(choices=MAPFORMAT_CHOICES, default=1)
    # manually open registration even if outside registration window
    allow_register = models.BooleanField(default=False)
    # when does registration open, and when does it close? specified when created in staff panel
    open_register = models.DateTimeField()
    # dont allow people to join once registration is closed
    close_register = models.DateTimeField()
    # when is the league going to start?
    start = models.DateTimeField()
    maps = models.ForeignKey(MapPoolChoice, related_name='league_maps', on_delete=models.PROTECT, null=True, blank=True)
    # the amount of credits that should be charged when joining
    req_credits = models.PositiveSmallIntegerField(default=0)
    size = models.PositiveSmallIntegerField(default=8)
    disable_userreport = models.BooleanField(default=False)
    prize1 = models.CharField(default='no prize specified', max_length=50)
    prize2 = models.CharField(default='no prize specified', max_length=50)
    prize3 = models.CharField(default='no prize specified', max_length=50)
    teams = models.ManyToManyField(LeagueTeam, blank=True)
    fa = models.ManyToManyField(LeagueFreeAgent, related_name="league_fas", blank=True)
    non_conference = models.ManyToManyField('matches.Match', related_name='non_conference_matches', blank=True)
    featured_matches = models.ManyToManyField('matches.Match', related_name='featured_matches', blank=True)
    featured_players = models.ManyToManyField('matches.Match', related_name='featured_players', blank=True)



