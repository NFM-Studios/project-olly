from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import IntegrityError
from profiles import UserProfile

from django.urls import reverse

class Team(models.Model):
    #team name
    name = models.CharField(max_length=25)
    #team bio
    about_us = models.CharField(max_length=250, default='Forever a mystery', blank=True)
    #not sure if we really need the earnings, but its here for now...
    total_earning = models.PositiveSmallIntegerField(default=0)
    # link your website in case its an org?
    website = models.CharField(max_length=100, default='No Website', blank=True)
    #link ur twitter, and maybe eventually embed the twitter feed
    twitter = models.CharField(max_length=15, default='No Twitter Linked', blank=True)
    #link ur twitch, maybe integrate the twitch api
    twitch = models.CharField(max_length=15, default='No Twitch Linked', blank=True)
    #whoever filled out the form to create the team, limited to only one
    founder = models.ForeignKey(User, related_name='founder', on_delete=models.CASCADE)
    #basically founder permissions, but to other people that didnt create the actual team
    captain = models.ManyToManyField(User, through='')
    #the people of the actual team, now a many to many, not a forkey
    players = models.ManyToManyField(User, through='TeamInvite', through_fields=('team', 'user'))
    #when they created the team
    created= models.DateTimeField(auto_now_add=True)
    #when they last updated anything in the team
    updated= models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Team'
        verbose_name_plural = 'Teams'
        ordering = ['updated']
    def get_players_count(self):
        return self.players.count()


class TeamInvite(models.Model):
    expire = models.DateTimeField(auto_now=False, auto_now_add=False)
    team = models.ForeignKey(Team, related_name='invited-to', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='to-invite', on_delete=models.CASCADE)
    inviter = models.ForeignKey(User, related_name='from-invite', on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    declined = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

class CaptainInvite(models.Model):
    expire = models.DateTimeField(auto_now=False, auto_now_add=False)
    team = models.ForeignKey(Team, related_name='invited-to', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='to-captain', on_delete=models.CASCADE)
    inviter = models.ForeignKey(User, related_name='from-captain', on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    declined = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
