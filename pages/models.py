from django.db import models

from singletournaments.models import SingleEliminationTournament


class SocialInfo(models.Model):
    class Meta:
        verbose_name_plural = "Social info"

    twitchchannel = models.URLField(verbose_name='twitch_channel', null=True, blank=True)
    youtubechannel = models.URLField(verbose_name='youtube_channel', null=True, blank=True)
    twitterprofile = models.URLField(verbose_name='twitter_profile', null=True, blank=True)
    facebookpage = models.URLField(verbose_name='facebook_page', null=True, blank=True)
    instagrampage = models.URLField(verbose_name='instagram_page', null=True, blank=True)

    stream = models.CharField(max_length=25, null=True, blank=True)


class StaticInfo(models.Model):
    class Meta:
        verbose_name_plural = "Static info"

    featured_tournament = models.ForeignKey(SingleEliminationTournament, related_name='featured_tournament',
                                            on_delete=models.SET_NULL, null=True, blank=True)
    about_us = models.TextField(default='about us')
    terms = models.TextField(default='terms of service')
    # privacy = models.TextField(default='privacy policy')

    slide1header = models.CharField(default="", max_length=50, blank=True, null=True)
    slide1subhead = models.CharField(default="", max_length=50, blank=True, null=True)
    slide1link = models.URLField(blank=True, null=True)
    slide1_img = models.ImageField(upload_to='carousel_images', blank=True)

    slide2header = models.CharField(default="", max_length=50, blank=True, null=True)
    slide2subhead = models.CharField(default="", max_length=50, blank=True, null=True)
    slide2link = models.URLField(blank=True, null=True)
    slide2_img = models.ImageField(upload_to='carousel_images', blank=True)

    slide3header = models.CharField(default="", max_length=50, blank=True, null=True)
    slide3subhead = models.CharField(default="", max_length=50, blank=True, null=True)
    slide3link = models.URLField(blank=True, null=True)
    slide3_img = models.ImageField(upload_to='carousel_images', blank=True)

    block1text = models.CharField(default="", max_length=50, blank=True, null=True)
    block1link = models.URLField(blank=True, null=True)
    block1_img = models.ImageField(upload_to='carousel_images', blank=True)

    block2text = models.CharField(default="", max_length=50, blank=True, null=True)
    block2link = models.URLField(blank=True, null=True)
    block2_img = models.ImageField(upload_to='carousel_images', blank=True)

    block3text = models.CharField(default="", max_length=50, blank=True, null=True)
    block3link = models.URLField(blank=True, null=True)
    block3_img = models.ImageField(upload_to='carousel_images', blank=True)

    welcomeln1 = models.CharField(default='welcome1', max_length=25, blank=True, null=True)
    welcomeln2 = models.CharField(default='welcome2', max_length=25, blank=True, null=True)


class Partner(models.Model):
    name = models.CharField(max_length=80)
    website = models.URLField(null=True, blank=True)
    twitter = models.CharField(max_length=100, default="#", blank=True)
    bio = models.TextField()
    logo = models.ImageField(upload_to='partner_images', blank=True)
