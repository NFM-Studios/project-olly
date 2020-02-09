from django.contrib.auth.models import User
from django.db import models

from profiles.models import UserProfile
from django_countries.fields import CountryField

from profiles.models import UserProfile


class Team(models.Model):
    # team name
    name = models.CharField(max_length=25)
    # team bio
    about_us = models.CharField(max_length=250, default='Forever a mystery', blank=True)
    # not sure if we really need the earnings, but its here for now...
    total_earning = models.PositiveSmallIntegerField(default=0)
    # link your website in case its an org?
    website = models.CharField(max_length=100, default='No Website', blank=True)
    # link ur twitter, and maybe eventually embed the twitter feed
    twitter = models.CharField(max_length=15, default='None Linked', blank=True)
    # link ur twitch, maybe integrate the twitch api
    twitch = models.CharField(max_length=15, default='None Linked', blank=True)
    # whoever filled out the form to create the team, limited to only one
    founder = models.ForeignKey(User, related_name='founder', on_delete=models.SET_NULL, null=True)
    # basically founder permissions, but to other people that didn't create the actual team
    captain = models.ManyToManyField(User, through='CaptainMembership', related_name='teamcaptain')
    # the people of the actual team, now a many to many, not a forkey
    players = models.ManyToManyField(User, through='TeamInvite', through_fields=('team', 'user', 'inviter'))
    # when they created the team
    created = models.DateTimeField(auto_now_add=True)
    # when they last updated anything in the team
    updated = models.DateTimeField(auto_now=True)
    # num field for the number of losses and wins
    num_matchloss = models.SmallIntegerField(default=0)
    num_matchwin = models.SmallIntegerField(default=0)

    num_wagerwin = models.SmallIntegerField(default=0)
    num_wagerloss = models.SmallIntegerField(default=0)
    # num field for the number of tournaments won
    num_tournywin = models.SmallIntegerField(default=0)
    numtournyloss = models.SmallIntegerField(default=0)

    totalxp = models.PositiveSmallIntegerField(default=0)
    rank = models.PositiveSmallIntegerField(default=100)

    country = CountryField(blank=True)

    image = models.ImageField(upload_to='team_images', blank=True)

    class Meta:
        verbose_name = 'Team'
        verbose_name_plural = 'Teams'
        ordering = ['updated']

    def get_players_count(self):
        return self.players.count()

    def website_linked(self):
        if not self.website:
            return True

    def get_total_xp(self):
        for invite in TeamInvite.objects.filter(team_id=self.id):
            userprofile = UserProfile.objects.get(user=invite.user)
            self.totalxp += userprofile.xp
        self.save()

    def get_rank(self):
        self.rank = int(Team.objects.filter(totalxp__gt=self.totalxp).count()) + 1
        self.save()

    def __str__(self):
        return self.name


class TeamInvite(models.Model):
    INVITE_CHOICES = (
        ('captain', 'Captain'),
        ('player', 'Player'),
    )
    expire = models.DateTimeField(auto_now=False, auto_now_add=False)
    team = models.ForeignKey(Team, related_name='invitedto', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='toinvite', on_delete=models.CASCADE)
    inviter = models.ForeignKey(User, related_name='frominvite', on_delete=models.CASCADE)
    captain = models.CharField(choices=INVITE_CHOICES, max_length=20, default='player')
    accepted = models.BooleanField(default=False)
    declined = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    hasPerms = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)


class CaptainMembership(models.Model):
    user = models.ForeignKey(User, related_name='captainperson', on_delete=models.CASCADE)
    team = models.ForeignKey(Team, related_name='team', on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
