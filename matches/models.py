from django.db import models
from matches.settings import GAME_CHOICES, PLATFORMS_CHOICES
from teams.models import Team

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

class MatchReport(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    # see the time the report was made for admins
