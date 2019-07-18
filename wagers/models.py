from django.db import models
from django.contrib.auth.models import User

from matches.models import GameChoice, PlatformChoice, Match
from matches.settings import MAPFORMAT_CHOICES, TEAMFORMAT_CHOICES
from teams.models import Team


class WagerChallenge(models.Model):
    team = models.ForeignKey(Team, related_name='challenge_team', on_delete=models.CASCADE)
    creator = models.ForeignKey(User, related_name='challenge_user', on_delete=models.CASCADE)
    info = models.TextField(default="No additional info given")
    time = models.DateTimeField(auto_now_add=True)
    confirm = models.BooleanField(default=False)


class WagerMatch(models.Model):
    match = models.ForeignKey(Match, related_name='match_obj', on_delete=models.CASCADE)
    credits = models.PositiveIntegerField(default=5)


class WagerRequest(models.Model):
    posted = models.DateTimeField(auto_now_add=True)
    team = models.ForeignKey(Team, related_name='requesting_team', on_delete=models.CASCADE)
    challenge_accepted = models.BooleanField(default=False)
    expiration = models.DateTimeField(null=True)
    expired = models.BooleanField(default=False)
    credits = models.PositiveIntegerField(default=5)
    game = models.ForeignKey(GameChoice, related_name='game_choices', on_delete=models.PROTECT)
    platform = models.ForeignKey(PlatformChoice, related_name='platform_choices', on_delete=models.PROTECT)
    bestof = models.SmallIntegerField(choices=MAPFORMAT_CHOICES, default=0)
    teamformat = models.SmallIntegerField(choices=TEAMFORMAT_CHOICES, default=1)
    info = models.TextField(default="No additional info given")
    creator = models.ForeignKey(User, related_name='creator_user', on_delete=models.CASCADE, null=True)
    challenge = models.ForeignKey(WagerChallenge, related_name='wager_challenge', on_delete=models.CASCADE, null=True)
    wmatch = models.ForeignKey(WagerMatch, null=True, blank=True, related_name='wmatch', on_delete=models.CASCADE)

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
