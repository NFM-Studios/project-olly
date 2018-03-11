from django.db import models
from matches.settings import GAME_CHOICES, PLATFORMS_CHOICES, TEAMFORMAT_CHOICES, MAPFORMAT_CHOICES
from teams.models import Team
from django.contrib.auth.models import User

# Create your models here.
class Match(models.Model):
    game = models.SmallIntegerField(choices=GAME_CHOICES, default=0)
    # default to ps4 for now bc why not
    platform = models.SmallIntegerField(choices=PLATFORMS_CHOICES, default=0)
    # assign the match to a tournament with a FK
    # tournament = models.ForeignKey()
    # fk fields for the 2 teams that are competiting,
    # verification for elgible teams happens within the tournament and teams app

    hometeam = models.ForeignKey(Team, related_name='hometeam')
    awayteam = models.ForeignKey(Team, related_name='awayteam')
    start = models.DateTimeField()
    # simple bool field to see if the match scores have been reported
    reported = models.BooleanField(default=False)
    # simple bool field to see if the entire match is completed
    completed = models.BooleanField(default=False)
    # field to declare the winner
    winner = models.ForeignKey(Team, related_name='champions')
    # set the default map format to best of 1
    bestof = models.SmallIntegerField(choices=MAPFORMAT_CHOICES, default=0)
    #          by default set it to be a 2v2.
    teamformat = models.SmallIntegerField(choices=TEAMFORMAT_CHOICES, default=1)

class MatchReport(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    # see the time the report was made for admins
    match = models.ForeignKey(Match, related_name='matchreporting')
    reporting_team = models.ForeignKey(Team, related_name='teamreporting')
    reporting_user = models.ForeignKey(User, related_name='userreporting')
    # who the person reporting is declaring the winner as
    reported_winner = models.ForeignKey(Team, related_name='winnerreporting')
