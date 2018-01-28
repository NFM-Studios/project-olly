from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import IntegrityError

from django.urls import reverse

class soloTeam(models.Model):
    name = models.CharField(max_length=25)
    about_me = models.CharField(max_length=250, default='Forever a mystery', blank=True)
    total_earning = models.PositiveSmallIntegerField(default=0)
    website = models.CharField(max_length=100, default='No Website', blank=True)
    twitter = models.CharField(max_length=15, default='No Twitter Linked', blank=True)
    twitch = models.CharField(max_length=15, default='No Twitch Linked', blank=True)
    founder = models.ForeignKey(User, related_name='solo-player', on_delete=models.CASCADE)
    created= models.DateTimeField(auto_now_add=True)
    updated= models.DateTimeField(auto_now=True)

class duoTeam(models.Model):
    name = models.CharField(max_length=25)
    about_me = models.CharField(max_length=250, default='Forever a mystery', blank=True)
    total_earning = models.PositiveSmallIntegerField(default=0)
    website = models.CharField(max_length=100, default='No Website', blank=True)
    twitter = models.CharField(max_length=15, default='No Twitter Linked', blank=True)
    twitch = models.CharField(max_length=15, default='No Twitch Linked', blank=True)
    founder = models.ForeignKey(User, related_name='duo-founder', on_delete=models.CASCADE)
    captain = models.ForeignKey(User, related_name='duo-captain', on_delete=models.CASCADE)
    player1 = models.ForeignKey(User, related_name='duo-player1', on_delete=models.CASCADE)
    player2 = models.ForeignKey(User, related_name='duo-player2', on_delete=models.CASCADE)
    created= models.DateTimeField(auto_now_add=True)
    updated= models.DateTimeField(auto_now=True)

class duoTeamInvite(models.Model):
    expire = models.DateTimeField(auto_now=False, auto_now_add=False)
    team = models.ForeignKey(duoTeam, related_name='invited-to', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user-invited', on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    declined = models.BooleanField(default=False)

class trioTeam(models.Model):
    name = models.CharField(max_length=25)
    about_me = models.CharField(max_length=250, default='Forever a mystery', blank=True)
    total_earning = models.PositiveSmallIntegerField(default=0)
    website = models.CharField(max_length=100, default='No Website', blank=True)
    twitter = models.CharField(max_length=15, default='No Twitter Linked', blank=True)
    twitch = models.CharField(max_length=15, default='No Twitch Linked', blank=True)
    founder = models.ForeignKey(User, related_name='trio-founder', on_delete=models.CASCADE)
    captain = models.ForeignKey(User, related_name='trio-captain', on_delete=models.CASCADE)
    player1 = models.ForeignKey(User, related_name='trio-player1', on_delete=models.CASCADE)
    player2 = models.ForeignKey(User, related_name='trio-player2', on_delete=models.CASCADE)
    player3 = models.ForeignKey(User, related_name='trio-player3', on_delete=models.CASCADE)
    created= models.DateTimeField(auto_now_add=True)
    updated= models.DateTimeField(auto_now=True)

class trioTeamInvite(models.Model):
    expire = models.DateTimeField(auto_now=False, auto_now_add=False)
    team = models.ForeignKey(duoTeam, related_name='invited-to', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user-invited', on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    declined = models.BooleanField(default=False)

class quadTeam(models.Model):
    name = models.CharField(max_length=25)
    about_me = models.CharField(max_length=250, default='Forever a mystery', blank=True)
    total_earning = models.PositiveSmallIntegerField(default=0)
    website = models.CharField(max_length=100, default='No Website', blank=True)
    twitter = models.CharField(max_length=15, default='No Twitter Linked', blank=True)
    twitch = models.CharField(max_length=15, default='No Twitch Linked', blank=True)
    founder = models.ForeignKey(User, related_name='quad-founder', on_delete=models.CASCADE)
    captain = models.ForeignKey(User, related_name='quad-captain', on_delete=models.CASCADE)
    player1 = models.ForeignKey(User, related_name='quad-player1', on_delete=models.CASCADE)
    player2 = models.ForeignKey(User, related_name='quad-player2', on_delete=models.CASCADE)
    player3 = models.ForeignKey(User, related_name='quad-player3', on_delete=models.CASCADE)
    player4 = models.ForeignKey(User, related_name='quad-player4', on_delete=models.CASCADE)
    created= models.DateTimeField(auto_now_add=True)
    updated= models.DateTimeField(auto_now=True)

class quadTeamInvite(models.Model):
    expire = models.DateTimeField(auto_now=False, auto_now_add=False)
    team = models.ForeignKey(duoTeam, related_name='invited-to', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user-invited', on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    declined = models.BooleanField(default=False)


class fiveTeam(models.Model):
    name = models.CharField(max_length=25)
    about_me = models.CharField(max_length=250, default='Forever a mystery', blank=True)
    total_earning = models.PositiveSmallIntegerField(default=0)
    website = models.CharField(max_length=100, default='No Website', blank=True)
    twitter = models.CharField(max_length=15, default='No Twitter Linked', blank=True)
    twitch = models.CharField(max_length=15, default='No Twitch Linked', blank=True)
    founder = models.ForeignKey(User, related_name='five-founder', on_delete=models.CASCADE)
    captain = models.ForeignKey(User, related_name='five-captain', on_delete=models.CASCADE)
    player1 = models.ForeignKey(User, related_name='five-player1', on_delete=models.CASCADE)
    player2 = models.ForeignKey(User, related_name='five-player2', on_delete=models.CASCADE)
    player3 = models.ForeignKey(User, related_name='five-player3', on_delete=models.CASCADE)
    player4 = models.ForeignKey(User, related_name='five-player4', on_delete=models.CASCADE)
    player5 = models.ForeignKey(User, related_name='five-player5', on_delete=models.CASCADE)
    created= models.DateTimeField(auto_now_add=True)
    updated= models.DateTimeField(auto_now=True)

class fiveTeamInvite(models.Model):
    expire = models.DateTimeField(auto_now=False, auto_now_add=False)
    team = models.ForeignKey(duoTeam, related_name='invited-to', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user-invited', on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    declined = models.BooleanField(default=False)

class sixTeam(models.Model):
    name = models.CharField(max_length=25)
    about_me = models.CharField(max_length=250, default='Forever a mystery', blank=True)
    total_earning = models.PositiveSmallIntegerField(default=0)
    website = models.CharField(max_length=100, default='No Website', blank=True)
    twitter = models.CharField(max_length=15, default='No Twitter Linked', blank=True)
    twitch = models.CharField(max_length=15, default='No Twitch Linked', blank=True)
    founder = models.ForeignKey(User, related_name='six-founder', on_delete=models.CASCADE)
    captain = models.ForeignKey(User, related_name='six-captain', on_delete=models.CASCADE)
    player1 = models.ForeignKey(User, related_name='six-player1', on_delete=models.CASCADE)
    player2 = models.ForeignKey(User, related_name='six-player2', on_delete=models.CASCADE)
    player3 = models.ForeignKey(User, related_name='six-player3', on_delete=models.CASCADE)
    player4 = models.ForeignKey(User, related_name='six-player4', on_delete=models.CASCADE)
    player5 = models.ForeignKey(User, related_name='six-player5', on_delete=models.CASCADE)
    player6 = models.ForeignKey(User, related_name='six-player6', on_delete=models.CASCADE)
    created= models.DateTimeField(auto_now_add=True)
    updated= models.DateTimeField(auto_now=True)

class sixTeamInvite(models.Model):
    expire = models.DateTimeField(auto_now=False, auto_now_add=False)
    team = models.ForeignKey(duoTeam, related_name='invited-to', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user-invited', on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    declined = models.BooleanField(default=False)
