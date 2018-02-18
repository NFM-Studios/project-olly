from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.


class UserProfile(models.Model):
    def __str__(self):
        return str(self.user)
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    xp = models.PositiveSmallIntegerField(default=0)
    credits = models.PositiveSmallIntegerField(default=0)
    total_earning = models.PositiveSmallIntegerField(default=0)
    about_me = models.CharField(max_length=500, default='Forever a mystery', blank=True)
    xbl = models.CharField(max_length=15, default='No Xbox Live Linked', blank=True)
    psn = models.CharField(max_length=16, default='No PSN Linked', blank=True)
    twitter_profile = models.CharField(max_length=15, default='No Twitter Linked', blank=True)
    twitch_channel = models.CharField(max_length=50, default='No Twitch Linked', blank=True)
    favorite_game = models.CharField(max_length=50, default='N/A', blank=True)
    favorite_console = models.CharField(max_length=50, default='N/A', blank=True)
    profile_picture = models.ImageField(upload_to='profile_images', blank=True)
    user_type = models.CharField(max_length=10, default='user')
    ip = models.CharField(max_length=16, default='0.0.0.0')


def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        user_profile = UserProfile(user=user)
        user_profile.save()


class BannedUser(models.Model):
    user = models.ForeignKey(User, related_name='banned', on_delete=models.CASCADE)
    ip = models.CharField(max_length=12, default='error')


post_save.connect(create_profile, sender=User)
