from django.db import models

# Create your models here.


class StaticInfo(models.Model):
    about_us = models.TextField(default='about us')
    terms = models.TextField(default='terms of service')
    privacy = models.TextField(default='privacy policy')
    stream = models.CharField(default='twitch', max_length=25)
    slide1link = models.TextField(default="#")
    slide2link = models.TextField(default="#")
    slide3link = models.TextField(default="#")

    # for steven

    # slide1_pic
    # slide2_pic
    # slide3_pic


class Partner(models.Model):
    name = models.CharField(max_length=80)
    website = models.CharField(max_length=100, default="#", blank=True)
    twitter = models.CharField(max_length=100, default="#", blank=True)
    bio = models.TextField()
    # logo = 