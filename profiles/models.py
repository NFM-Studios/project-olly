from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django_countries.fields import CountryField

NOTIFICATION_TYPES = [
    ('match', 1),
    ('tournament', 2),
    ('league', 3),
    ('team', 4),
    ('support', 5),
    ('news', 6),
    ('general', 7),
    ('store', 8),
]


class Notification(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(default="No description given")
    # set the default sender of a notification as "System"
    sender = models.CharField(max_length=255, default="System")
    type = models.CharField(choices=NOTIFICATION_TYPES, default='general', max_length=255)
    datetime = models.DateTimeField(auto_created=True, auto_now_add=True, blank=True)
    link = models.CharField(max_length=255)
    pk1 = models.IntegerField(default=0)
    # has the user marked the notification as read? default to false
    read = models.BooleanField(default=False)
    # has the user visited the notification list page since the notification was generated? used for stats
    seen = models.BooleanField(default=False)


class UserProfile(models.Model):
    def __str__(self):
        return str(self.user)

    # associate the userprofile with the django user
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    alternate_name = models.CharField(blank=True, null=True, max_length=50)
    # xp they have from winning events
    xp = models.PositiveSmallIntegerField(default=0)
    # all notifications associated with this user
    notifications = models.ManyToManyField(Notification, related_name='user_notifications', blank=True)
    # credits they own from purchasing things in the store
    credits = models.PositiveSmallIntegerField(default=0)
    passes = models.PositiveSmallIntegerField(default=0)
    # amount of money they have cashed out
    total_earning = models.PositiveSmallIntegerField(default=0)
    current_earning = models.PositiveSmallIntegerField(default=0)
    about_me = models.TextField(default='Forever a mystery', blank=True)
    steamid64 = models.CharField(max_length=255, default='No SteamID64', blank=True)
    discord = models.CharField(max_length=255, default='No Discord', blank=True)
    xbl = models.CharField(max_length=30, default='No Xbox Live Linked', blank=True)
    psn = models.CharField(max_length=30, default='No PSN Linked', blank=True)
    steam = models.CharField(max_length=30, default='No Steam Linked', blank=True)
    epic = models.CharField(max_length=30, default='No Epic Linked', blank=True)
    lol = models.CharField(max_length=30, default='No LOL Linked', blank=True)
    battlenet = models.CharField(max_length=30, default='No Battle.net Linked', blank=True)
    activisionid = models.CharField(max_length=30, default='No Activision ID Linked', blank=True)
    twitter_profile = models.CharField(max_length=30, default='No Twitter Linked', blank=True)
    twitch_channel = models.CharField(max_length=50, default='No Twitch Linked', blank=True)
    favorite_game = models.CharField(max_length=50, default='N/A', blank=True)
    favorite_console = models.CharField(max_length=50, default='N/A', blank=True)
    profile_picture = models.ImageField(upload_to='profile_images', blank=True)
    USER_TYPE_CHOICES = [
        ('user', 'Standard User'),
        ('admin', 'Admin'),
        ('superadmin', 'Super Admin')
    ]
    user_type = models.CharField(max_length=10, default='user', choices=USER_TYPE_CHOICES)
    ip = models.CharField(max_length=45, default='0.0.0.0')
    num_trophies = models.PositiveSmallIntegerField(default=0)
    xbl_verified = models.BooleanField(default=False, null=False, blank=True)
    psn_verified = models.BooleanField(default=False, null=False, blank=False)
    user_verified = models.BooleanField(default=False, null=False, blank=True)
    # default trophies
    num_bronze = models.PositiveSmallIntegerField(default=0)
    num_silver = models.PositiveSmallIntegerField(default=0)
    num_gold = models.PositiveSmallIntegerField(default=0)

    # just in case we need them later on...
    num_plat = models.PositiveSmallIntegerField(default=0)
    num_diamond = models.PositiveSmallIntegerField(default=0)
    num_titanium = models.PositiveSmallIntegerField(default=0)

    num_wagerwin = models.PositiveIntegerField(default=0)
    num_wagerloss = models.PositiveIntegerField(default=0)

    tournament_wins = models.PositiveSmallIntegerField(default=0)
    dubl_tournament_wins = models.PositiveSmallIntegerField(default=0)

    rank = models.PositiveSmallIntegerField(default=100)
    # country the dude lives in.
    country = CountryField(blank_label='(select country)', default='US')

    email_enabled = models.BooleanField(default=True)
    # teams the user founded
    founder_teams = models.ManyToManyField('teams.Team', related_name='profile_founder_teams', blank=True)
    # teams the user is a captain of
    captain_teams = models.ManyToManyField('teams.Team', related_name='profile_captain_teams', blank=True)
    # teams the user is a player on
    player_teams = models.ManyToManyField('teams.Team', related_name='profile_player_teams', blank=True)

    def calculate_rank(self):
        self.rank = int(UserProfile.objects.filter(xp__gt=self.xp).count()) + 1
        self.save()


def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        user_profile = UserProfile(user=user)
        user_profile.save()


class BannedUser(models.Model):
    user = models.ForeignKey(User, related_name='banned', on_delete=models.CASCADE)
    ip = models.CharField(max_length=12, default='error')


post_save.connect(create_profile, sender=User)
