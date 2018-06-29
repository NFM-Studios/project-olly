from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django_countries.fields import CountryField
from django.dispatch import receiver

# Create your models here.


class UserGear(models.Model):
    user = models.ForeignKey(User, related_name='userspecs', on_delete=models.CASCADE)
    # see if the guy actually owns a pc
    ownpc = models.BooleanField(default=False)

    cpu = models.CharField(max_length=30, default='No CPU specified')
    gpu = models.CharField(max_length=30, default='No GPU specified')
    psu = models.CharField(max_length=30, default='No PSU specified')
    case = models.CharField(max_length=30, default='No Case specified')
    os = models.CharField(max_length=30, default='No OS specified')


class UserProfile(models.Model):
    def __str__(self):
        return str(self.user)

    # associate the userprofile with the django user
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    # xp they have from winning events
    xp = models.PositiveSmallIntegerField(default=0)
    # credits they own from purchasing things in the store
    credits = models.PositiveSmallIntegerField(default=0)
    passes = models.PositiveSmallIntegerField(default=0)
    # amount of money they have cashed out
    total_earning = models.PositiveSmallIntegerField(default=0)
    current_earning = models.PositiveSmallIntegerField(default=0)
    about_me = models.TextField(default='Forever a mystery', blank=True)
    xbl = models.CharField(max_length=30, default='No Xbox Live Linked', blank=True)
    psn = models.CharField(max_length=30, default='No PSN Linked', blank=True)
    steam = models.CharField(max_length=30, default='No Steam Linked', blank=True)
    lol = models.CharField(max_length=30, default='No LOL Linked', blank=True)
    battlenet = models.CharField(max_length=30, default='No Battle.net Linked', blank=True)
    twitter_profile = models.CharField(max_length=30, default='No Twitter Linked', blank=True)
    twitch_channel = models.CharField(max_length=50, default='No Twitch Linked', blank=True)
    favorite_game = models.CharField(max_length=50, default='N/A', blank=True)
    favorite_console = models.CharField(max_length=50, default='N/A', blank=True)
    profile_picture = models.ImageField(upload_to='profile_images', blank=True)
    user_type = models.CharField(max_length=10, default='user')
    ip = models.CharField(max_length=16, default='0.0.0.0')
    num_trophies = models.PositiveSmallIntegerField(default=0)
    xbl_verified = models.BooleanField(default=False, null=False, blank=True)
    psn_verified = models.BooleanField(default=False, null=False, blank=False)
    # default trophies
    num_bronze = models.PositiveSmallIntegerField(default=0)
    num_silver = models.PositiveSmallIntegerField(default=0)
    num_gold = models.PositiveSmallIntegerField(default=0)

    # just in case we need them later on...
    num_plat = models.PositiveSmallIntegerField(default=0)
    num_diamond = models.PositiveSmallIntegerField(default=0)
    num_titanium = models.PositiveSmallIntegerField(default=0)

    tournament_wins = models.PositiveSmallIntegerField(default=0)
    dubl_tournament_wins = models.PositiveSmallIntegerField(default=0)

    # country the dude lives in.
    country = CountryField(blank_label='(select country)', default='US')


def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        user_profile = UserProfile(user=user)
        user_profile.save()


class BannedUser(models.Model):
    user = models.ForeignKey(User, related_name='banned', on_delete=models.CASCADE)
    ip = models.CharField(max_length=12, default='error')


@receiver(models.signals.post_delete, sender=UserProfile)
# This should never be run in theory. It would only be hit if the UserProfile was completely deleted
def auto_delete_file(sender, instance, **kwargs):
    if instance.profile_picture:
        instance.profile_picture.delete()


@receiver(models.signals.pre_save, sender=UserProfile)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_file = UserProfile.objects.get(pk=instance.pk).profile_picture
    except UserProfile.DoesNotExist:
        return False

    new_file = instance.profile_picture
    if not old_file == new_file:
        old_file.delete(save=False)


post_save.connect(create_profile, sender=User)
