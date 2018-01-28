from django.db import models

# Create your models here.
class soloTeam(models.Model):
    about_me = models.CharField(max_length=250, default='Forever a mystery', blank=True)
    total_earning = models.PositiveSmallIntegerField(default=0)
    website = models.CharField(max_length=100, default='No Website', blank=True)
    twitter = models.CharField(max_length=15, default='No Twitter Linked', blank=True)

class soloTeamPlayer
    team = models.ForeignKey(User, related_name='team', on_delete=models.CASCADE)

class duoTeam(models.Model):

class duoTeamPlayer
