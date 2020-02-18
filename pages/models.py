from django.db import models

from singletournaments.models import SingleEliminationTournament


class SocialInfo(models.Model):
    twitchchannel = models.URLField(verbose_name='twitch_channel', null=True, blank=True,
                                    default='https://www.twitch.tv')
    youtubechannel = models.URLField(verbose_name='youtube_channel', null=True, blank=True,
                                     default='https://www.youtube.com')
    twitterprofile = models.URLField(verbose_name='twitter_profile', null=True, blank=True,
                                     default='https://www.twitter.com')
    facebookpage = models.URLField(verbose_name='facebook_page', null=True, blank=True,
                                   default='https://www.facebook.com')
    instagrampage = models.URLField(verbose_name='instagram_page', null=True, blank=True,
                                    default='https://www.instagram.com')

    stream = models.CharField(default='twitch', max_length=25)


class StaticInfo(models.Model):
    featured_tournament = models.ForeignKey(SingleEliminationTournament, related_name='featured_tournament',
                                            on_delete=models.SET_NULL, null=True, blank=True)
    about_us = models.TextField(default='about us')
    terms = models.TextField(default='terms of service')
    # privacy = models.TextField(default='privacy policy')

    slide1link = models.TextField(default="https://www.google.com", blank=True, null=True)
    slide2link = models.TextField(default="https://www.google.com", blank=True, null=True)
    slide3link = models.TextField(default="https://www.google.com", blank=True, null=True)
    slide1_img = models.ImageField(upload_to='carousel_images', blank=True)
    slide2_img = models.ImageField(upload_to='carousel_images', blank=True)
    slide3_img = models.ImageField(upload_to='carousel_images', blank=True)
    welcomeln1 = models.CharField(default='welcome1', max_length=25, blank=True, null=True)
    welcomeln2 = models.CharField(default='welcome2', max_length=25, blank=True, null=True)


class Partner(models.Model):
    name = models.CharField(max_length=80)
    website = models.URLField(default="https://www.google.com", blank=True)
    twitter = models.CharField(max_length=100, default="#", blank=True)
    bio = models.TextField()
    logo = models.ImageField(upload_to='partner_images', blank=True)
