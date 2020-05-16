from django.db import models
from teams.models import Team
from matches.models import Match, GameChoice, PlatformChoice, MapPoolChoice, MapChoice, SportChoice
from matches.settings import TEAMFORMAT_CHOICES, MAPFORMAT_CHOICES
from singletournaments.models import SingleTournamentRuleset


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
    # W=Win, L=Loss, OTL=Overtime Loss, T=Tie, OTW=Overtime Win, OTT=Overtime Tie
    RECORD_FORMAT_CHOICES = (
        (1, "W-L-OTL"),
        (2, "W-L-T"),
        (3, "W-L-OTW-OTL"),
        (4, "W-L-OTW-OTL-OTT"),
        (5, "W-L"),
    )
    # record format to show on front end
    record_format = models.CharField(choices=RECORD_FORMAT_CHOICES, default="W-L-OTL", max_length=20)
    # number of divisions to break teams into
    num_divisons = models.PositiveSmallIntegerField(default=2)
    # max amount of teams to allow into a division
    max_division_size = models.PositiveSmallIntegerField(default=5)


class LeagueTeam(models.Model):
    team = models.ForeignKey(Team, related_name='league_team', on_delete=models.PROTECT)
    wins = models.PositiveSmallIntegerField(default=0)
    losses = models.PositiveSmallIntegerField(default=0)
    ot_losses = models.PositiveSmallIntegerField(default=0)
    ot_wins = models.PositiveSmallIntegerField(default=0)
    ties = models.PositiveSmallIntegerField(default=0)


class LeagueDivision(models.Model):
    # name for the league division - set to null in case admins wish to manually change it
    name = models.CharField(null=True, max_length=50)
    # teams that are in that division, allow it to be empty
    teams = models.ManyToManyField(LeagueTeam, blank=True)
    # games that are to be played and have been played in that division, blank until all matches are generated
    games = models.ManyToManyField(Match, blank=True)


class League(models.Model):
    name = models.CharField(default="League Name", max_length=50)
    settings = models.ForeignKey(LeagueSettings, related_name="league_settings", on_delete=models.PROTECT)
    ruleset = models.ForeignKey(SingleTournamentRuleset, related_name="league_ruleset", on_delete=models.PROTECT)
    # if set to true the league will display on the front page, false and it will not
    active = models.BooleanField(default=False)
    info = models.TextField(default="No information provided")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    divisions = models.ManyToManyField(LeagueDivision, blank=True)
    platform = models.ForeignKey(PlatformChoice, related_name='league_platform', on_delete=models.PROTECT, null=True)
    game = models.ForeignKey(GameChoice, related_name='league_game', on_delete=models.PROTECT, null=True)
    sport = models.ForeignKey(SportChoice, related_name='league_sport', on_delete=models.PROTECT, null=True)
    image = models.ImageField(upload_to='league_images', blank=True)
    # team format, ex 1v1, 2v2, 3v3, 4v4, 5v5, 6v6
    teamformat = models.SmallIntegerField(choices=TEAMFORMAT_CHOICES, default=1)
    # by default its a best of 1. Not sure if we need this here. Finals might be best of 3, etc in
    # the future possibly. TBD. For now this will work though.
    bestof = models.SmallIntegerField(choices=MAPFORMAT_CHOICES, default=0)
    # manually open registration even if outside registration window
    allow_register = models.BooleanField(default=False)
    # when does registration open, and when does it close? specified when created in staff panel
    open_register = models.DateTimeField()
    # dont allow people to join once registration is closed
    close_register = models.DateTimeField()
    # when is the league going to start?
    start = models.DateTimeField()
    maps = models.ForeignKey(MapPoolChoice, related_name='league_maps', on_delete=models.PROTECT, null=True)



