from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import IntegrityError
from profiles import UserProfile

from django.urls import reverse

class Team(models.Model):
    name = models.CharField(max_length=25)
    about_us = models.CharField(max_length=250, default='Forever a mystery', blank=True)
    total_earning = models.PositiveSmallIntegerField(default=0)
    website = models.CharField(max_length=100, default='No Website', blank=True)
    twitter = models.CharField(max_length=15, default='No Twitter Linked', blank=True)
    twitch = models.CharField(max_length=15, default='No Twitch Linked', blank=True)
    founder = models.ForeignKey(User, related_name='founder', on_delete=models.CASCADE)
    captain = models.ForeignKey(User, related_name='captain', on_delete=models.CASCADE)
    players = models.ManyToManyField(Player, through='TeamInvite', through_fields=('team', 'user'))
    created= models.DateTimeField(auto_now_add=True)
    updated= models.DateTimeField(auto_now=True)

class TeamInvite(models.Model):
    expire = models.DateTimeField(auto_now=False, auto_now_add=False)
    team = models.ForeignKey(Team, related_name='invited-to', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user-invited', on_delete=models.CASCADE)
    inviter = models.ForeignKey(User, related_name='team_invites', on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    declined = models.BooleanField(default=False)
