from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    use_2fa = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    xp = models.PositiveSmallIntegerField(default=0)
    credits = models.PositiveSmallIntegerField(default=0)
    total_earning = models.PositiveSmallIntegerField(default=0)
    about_me = models.CharField(max_length=500, default='')
    xbl = models.CharField(max_length=15, default='')
    psn = models.CharField(max_length=16, default='')
    twitter_profile = models.CharField(max_length=15, default='')
    twitch_channel = models.CharField(max_length=50, default='')
    favorite_game = models.CharField(max_length=50, default='')
    favorite_console = models.CharField(max_length=50, default='')
    profile_picture = models.URLField(max_length=200, default='')

def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User)
