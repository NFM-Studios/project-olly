from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver

from matches.settings import TEAMFORMAT_CHOICES, MAPFORMAT_CHOICES
from teams.models import Team


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

    #def add_map(self, mappk):
    #    newmap = MapChoice.objects.get(id=mappk)
    #    newmap.map_num = self.maps.count() + 1
    #    self.maps.add(newmap)

    def __str__(self):
        return self.name


class Match(models.Model):
    type = models.CharField(blank=True, null=True, max_length=20)
    matchnum = models.SmallIntegerField(default=0)
    map = models.ForeignKey(MapChoice, related_name='match_map', on_delete=models.CASCADE, null=True)
    game = models.ForeignKey(GameChoice, related_name='GameChoice', on_delete=models.CASCADE)
    # default to ps4 for now bc why not
    platform = models.ForeignKey(PlatformChoice, related_name='PlatformChoice', on_delete=models.CASCADE)
    # assign the match to a tournament with a FK
    # tournament = models.ForeignKey(SingleEliminationTournament, related_name='tournament', on_delete=models.CASCADE)
    # fk fields for the 2 teams that are competiting,
    # verification for elgible teams happens within the tournament and teams app
    # home team is team 1
    hometeam = models.ForeignKey(Team, related_name='hometeam', on_delete=models.CASCADE, null=True)
    # away team is team 2
    awayteam = models.ForeignKey(Team, related_name='awayteam', on_delete=models.CASCADE, null=True)
    # simple bool field to see if the match scores have been reported
    reported = models.BooleanField(default=False)
    # simple bool field to see if the entire match is completed
    completed = models.BooleanField(default=False)
    # field to declare the winner
    winner = models.ForeignKey(Team, related_name='champions', on_delete=models.CASCADE, null=True)
    loser = models.ForeignKey(Team, related_name='loser', on_delete=models.CASCADE, null=True)
    # set the default map format to best of 1
    bestof = models.SmallIntegerField(choices=MAPFORMAT_CHOICES, default=0)
    #          by default set it to be a 2v2.
    teamformat = models.SmallIntegerField(choices=TEAMFORMAT_CHOICES, default=1)

    team1reported = models.BooleanField(default=False)
    team1reportedwinner = models.ForeignKey(Team, related_name='team1reportedwinner', on_delete=models.CASCADE,
                                            null=True, blank=True)
    team2reported = models.BooleanField(default=False)
    team2reportedwinner = models.ForeignKey(Team, related_name='team2reportedwinner', on_delete=models.CASCADE,
                                            null=True, blank=True)

    info = models.TextField(default="Match Info: ")

    disputed = models.BooleanField(default=False)

    bye_1 = models.BooleanField(default=False)

    bye_2 = models.BooleanField(default=False)

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


class MatchReport(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    # see the time the report was made for admins
    match = models.ForeignKey(Match, related_name='matchreporting', on_delete=models.CASCADE)
    reporting_team = models.ForeignKey(Team, related_name='teamreporting', on_delete=models.CASCADE)
    reporting_user = models.ForeignKey(User, related_name='userreporting', on_delete=models.CASCADE)
    # who the person reporting is declaring the winner as
    reported_winner = models.ForeignKey(Team, related_name='winnerreporting', on_delete=models.CASCADE)
    proof = models.CharField(max_length=300, default='no text inserted', blank=False)


class MatchDispute(models.Model):
    # save when it  was created and last  updated
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # save the 2 teams that are  involved in the match,  and thus involved in this dispute
    # team1 should line up to team1 of the original match, and same for team2.
    team1 = models.ForeignKey(Team, related_name='team1', on_delete=models.CASCADE)
    team2 = models.ForeignKey(Team, related_name='team2', on_delete=models.CASCADE)

    # the match object that is currently being disputed
    match = models.ForeignKey(Match, related_name='disputedMatch', on_delete=models.CASCADE)

    # proof  that each team submits to an admin
    # teamproof = models.CharField(max_length=300, default='(team 1) no text inserted', blank=False)
    teamproof_1 = models.URLField(blank=False)
    teamproof_2 = models.URLField(blank=True)
    teamproof_3 = models.URLField(blank=True)
    # who submitted the original match report, hence causing this dispute
    team1origreporter = models.ForeignKey(User, related_name='team1OriginalReporter', on_delete=models.CASCADE)
    team2origreporter = models.ForeignKey(User, related_name='team2OriginalReporter', on_delete=models.CASCADE)

    # who is submitting the proof for the dispute
    teamreporter = models.ForeignKey(User, related_name='team1Disputer', on_delete=models.CASCADE, null=True,
                                     blank=True)

    # once all this information is submitted it will be viewable  by an admin that will look at the proof and
    # determine who the winner is.


@receiver(models.signals.post_delete, sender=GameChoice)
# This should never be run in theory. It would only be hit if the Post was completely deleted
def auto_delete_file(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete()


@receiver(models.signals.pre_save, sender=GameChoice)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_file = GameChoice.objects.get(pk=instance.pk).image
    except GameChoice.DoesNotExist:
        return False

    new_file = instance.image
    if not old_file == new_file:
        old_file.delete(save=False)


@receiver(models.signals.post_delete, sender=PlatformChoice)
# This should never be run in theory. It would only be hit if the Post was completely deleted
def auto_delete_file(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete()


@receiver(models.signals.pre_save, sender=PlatformChoice)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_file = PlatformChoice.objects.get(pk=instance.pk).image
    except PlatformChoice.DoesNotExist:
        return False

    new_file = instance.image
    if not old_file == new_file:
        old_file.delete(save=False)
