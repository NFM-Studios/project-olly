from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import IntegrityError
# from profiles import UserProfile

from django.urls import reverse


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
    twitter = models.CharField(max_length=15, default='No Twitter Linked', blank=True)
    # link ur twitch, maybe integrate the twitch api
    twitch = models.CharField(max_length=15, default='No Twitch Linked', blank=True)
    # whoever filled out the form to create the team, limited to only one
    founder = models.ForeignKey(User, related_name='founder', on_delete=models.CASCADE)
    # basically founder permissions, but to other people that didn't create the actual team
    captain = models.ManyToManyField(User, through='CaptainMembership', related_name='teamcaptain')
    # the people of the actual team, now a many to many, not a forkey
    players = models.ManyToManyField(User, through='TeamInvite', through_fields=('team', 'user', 'inviter'))
    # when they created the team
    created = models.DateTimeField(auto_now_add=True)
    # when they last updated anything in the team
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Team'
        verbose_name_plural = 'Teams'
        ordering = ['updated']

    def get_players_count(self):
        return self.players.count()

    def website_linked(self):
        if not self.website:
            return True

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


class CaptainMembership(models.Model):
    user = models.ForeignKey(User, related_name='captainperson', on_delete=models.CASCADE)
    team = models.ForeignKey(Team, related_name='team', on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
