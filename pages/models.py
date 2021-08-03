import ckeditor.fields
from django.db import models

from singletournaments.models import SingleEliminationTournament
from ckeditor.fields import RichTextField


class OllySetting(models.Model):
    class Meta:
        verbose_name_plural = "Olly Settings"

    freeze_team_invites = models.BooleanField(default=False)
    disable_team_creation = models.BooleanField(default=False)
    freeze_team_leaves = models.BooleanField(default=False)
    freeze_team_deletion = models.BooleanField(default=False)
    freeze_team_player_removal = models.BooleanField(default=False)
    whats_new = RichTextField(default='')

    def can_invite(self):
        try:
            if OllySetting.objects.get(pk=1).freeze_team_invites:
                return False
            else:
                return True
        except:
            return False

    def can_create_team(self):
        try:
            if OllySetting.objects.get(pk=1).disable_team_creation:
                return False
            else:
                return True
        except:
            return False


class StaticPage(models.Model):
    slug = models.SlugField(max_length=50)
    page_name = models.CharField(max_length=50, blank=False, null=False)
    content = RichTextField(default='')
    redirects = models.BooleanField(default=False)
    url = models.URLField(max_length=200, blank=True)


class FrontPageSlide(models.Model):
    class Meta:
        verbose_name_plural = "Front Page Slides"

    header = models.CharField(default="", max_length=50, blank=True, null=True)
    subhead = models.CharField(default="", max_length=100, blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='carousel_images', blank=True)


class SocialInfo(models.Model):
    class Meta:
        verbose_name_plural = "Social info"

    twitchchannel = models.URLField(verbose_name='twitch_channel', null=True, blank=True)
    youtubechannel = models.URLField(verbose_name='youtube_channel', null=True, blank=True)
    twitterprofile = models.URLField(verbose_name='twitter_profile', null=True, blank=True)
    facebookpage = models.URLField(verbose_name='facebook_page', null=True, blank=True)
    instagrampage = models.URLField(verbose_name='instagram_page', null=True, blank=True)
    discord = models.URLField(verbose_name="discord_server", null=True, blank=True)

    stream = models.CharField(max_length=25, null=True, blank=True)


class StaticInfo(models.Model):
    class Meta:
        verbose_name_plural = "Static info"

    featured_tournament = models.ForeignKey(SingleEliminationTournament, related_name='featured_tournament',
                                            on_delete=models.SET_NULL, null=True, blank=True)
    about_us = models.TextField(default='about us')
    terms = models.TextField(default='terms of service')
    # privacy = models.TextField(default='privacy policy')

    block1text = models.CharField(default="", max_length=50, blank=True, null=True)
    block1link = models.URLField(blank=True, null=True)
    block1_img = models.ImageField(upload_to='carousel_images', blank=True)

    block2text = models.CharField(default="", max_length=50, blank=True, null=True)
    block2link = models.URLField(blank=True, null=True)
    block2_img = models.ImageField(upload_to='carousel_images', blank=True)

    block3text = models.CharField(default="", max_length=50, blank=True, null=True)
    block3link = models.URLField(blank=True, null=True)
    block3_img = models.ImageField(upload_to='carousel_images', blank=True)


class Partner(models.Model):
    name = models.CharField(max_length=80)
    website = models.URLField(null=True, blank=True)
    twitter = models.CharField(max_length=100, default="#", blank=True)
    bio = models.TextField()
    logo = models.ImageField(upload_to='partner_images', blank=True)
