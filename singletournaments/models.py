from django.db import models
from matches.settings import GAME_CHOICES, PLATFORMS_CHOICES
from teams.models import Team


class SingleEliminationTournament(models.Model):

    open_register = models.DateTimeField()
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
    # what will they win?
    prize = models.CharField
    # all the teams that are in the event. elgibility happens inside the view, when they try to register
    teams = models.ManyToManyField()
    # specify the winning team when they are declared
    winner = models.ForeignKey(Team, related_name='winningteam')
    # specify second place, just for storage and future reference
    second = models.ForeignKey(Team, related_name='secondplaceteam')
    # specify how many teams the event will be capped at, and the size of the bracket
    size = models.PositiveSmallIntegerField(default=32)

    # need to figure out how we will work rules
    rules = models.ForeignKey(RuleSet, related_name='tournamentrules')


class RuleSet(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    text = models.TextField()
