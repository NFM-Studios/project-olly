from django.db import models
from django.dispatch import receiver

from singletournaments.models import SingleEliminationTournament


class StaticInfo(models.Model):
    featured_touranment = models.ForeignKey(SingleEliminationTournament, related_name='featured_tournamet',
                                            on_delete=models.CASCADE, null=True)
    about_us = models.TextField(default='about us')
    terms = models.TextField(default='terms of service')
    # privacy = models.TextField(default='privacy policy')
    stream = models.CharField(default='twitch', max_length=25)
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
    slide1link = models.TextField(default="https://www.google.com", blank=True, null=True)
    slide2link = models.TextField(default="https://www.google.com", blank=True, null=True)
    slide3link = models.TextField(default="https://www.google.com", blank=True, null=True)
    slide1_img = models.ImageField(upload_to='carousel_images', blank=True)
    slide2_img = models.ImageField(upload_to='carousel_images', blank=True)
    slide3_img = models.ImageField(upload_to='carousel_images', blank=True)
    welcomeln1 = models.CharField(default='welcome1', max_length=25, blank=True, null=True)
    welcomeln2 = models.CharField(default='welcome2', max_length=25, blank=True, null=True)

    bingeslide1big = models.TextField(default="Coming Soon!", blank=True, null=True)
    bingeslide1small = models.TextField(default="Coming Soon!", blank=True, null=True)
    bingeslide1link = models.URLField(max_length=200, default="https://www.google.com", blank=True, null=True)

    bingeslide2big = models.TextField(default="Coming Soon!", blank=True, null=True)
    bingeslide2small = models.TextField(default="Coming Soon!", blank=True, null=True)
    bingeslide2link = models.URLField(max_length=200, default='https://www.google.com', blank=True, null=True)

    bingeslide3big = models.TextField(default="Coming Soon!", blank=True, null=True)
    bingeslide3small = models.TextField(default="Coming Soon!", blank=True, null=True)
    bingeslide3link = models.URLField(max_length=200, default="https://www.google.com", blank=True, null=True)

    bingetop1 = models.TextField(default="Coming Soon!", blank=True, null=True)
    bingetop1image = models.ImageField(upload_to='carousel_images', blank=True)
    bingetop1link = models.URLField(max_length=200, default="https://www.google.com", blank=True, null=True)
    bingetop1linktxt = models.TextField(default="Coming Soon!", blank=True, null=True)

    bingetop2 = models.TextField(default="Coming Soon!", blank=True, null=True)
    bingetop2image = models.ImageField(upload_to='carousel_images', blank=True)
    bingetop2link = models.URLField(max_length=200, default="https://www.google.com", blank=True, null=True)
    bingetop2linktxt = models.TextField(default="Coming Soon!", blank=True, null=True)

    bingetop3 = models.TextField(default="Coming Soon!", blank=True, null=True)
    bingetop3image = models.ImageField(upload_to='carousel_images', blank=True)
    bingetop3link = models.URLField(max_length=200, default="https://www.google.com", blank=True, null=True)
    bingetop3linktxt = models.TextField(default="Coming Soon!", blank=True, null=True)

    bingetop4 = models.TextField(default="Coming Soon!", blank=True, null=True)
    bingetop4image = models.ImageField(upload_to='carousel_images', blank=True)
    bingetop4link = models.URLField(max_length=200, default="https://www.google.com", blank=True, null=True)
    bingetop4linktxt = models.TextField(default="Coming Soon!", blank=True, null=True)


class Partner(models.Model):
    name = models.CharField(max_length=80)
    website = models.URLField(default="https://www.google.com", blank=True)
    twitter = models.CharField(max_length=100, default="#", blank=True)
    bio = models.TextField()
    logo = models.ImageField(upload_to='partner_images', blank=True)


@receiver(models.signals.post_delete, sender=Partner)
def auto_delete_file(sender, instance, **kwargs):
    if instance.logo:
        instance.logo.delete()


@receiver(models.signals.pre_save, sender=Partner)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_file = Partner.objects.get(pk=instance.pk).logo
    except Partner.DoesNotExist:
        return False

    new_file = instance.logo
    if not old_file == new_file:
        old_file.delete(save=False)


@receiver(models.signals.post_delete, sender=StaticInfo)
def auto_delete_file(sender, instance, **kwargs):
    if instance.slide1_img:
        instance.slide1_img.delete()
    if instance.slide2_img:
        instance.slide2_img.delete()
    if instance.slide3_img:
        instance.slide3_img.delete()
    if instance.bingetop1image:
        instance.bingetop1image.delete()
    if instance.bingetop2image:
        instance.bingetop2image.delete()
    if instance.bingetop3image:
        instance.bingetop3image.delete()
    if instance.bingetop4image:
        instance.bingetop4image.delete()


@receiver(models.signals.pre_save, sender=StaticInfo)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    # Slide 1
    try:
        old_slide1 = StaticInfo.objects.get(pk=instance.pk).slide1_img
    except StaticInfo.DoesNotExist:
        return False

    new_slide1 = instance.slide1_img
    if not old_slide1 == new_slide1:
        old_slide1.delete(save=False)

    # Slide 2
    try:
        old_slide2 = StaticInfo.objects.get(pk=instance.pk).slide2_img
    except StaticInfo.DoesNotExist:
        return False

    new_slide2 = instance.slide2_img
    if not old_slide2 == new_slide2:
        old_slide2.delete(save=False)

    # Slide 3
    try:
        old_slide3 = StaticInfo.objects.get(pk=instance.pk).slide3_img
    except StaticInfo.DoesNotExist:
        return False

    new_slide3 = instance.slide3_img
    if not old_slide3 == new_slide3:
        old_slide3.delete(save=False)

    # Binge top 1
    try:
        old_top1 = StaticInfo.objects.get(pk=instance.pk).bingetop1image
    except StaticInfo.DoesNotExist:
        return False

    new_top1 = instance.bingetop1image
    if not old_top1 == new_top1:
        old_top1.delete(save=False)

    # Binge top 2
    try:
        old_top2 = StaticInfo.objects.get(pk=instance.pk).bingetop2image
    except StaticInfo.DoesNotExist:
        return False

    new_top2 = instance.bingetop2image
    if not old_top2 == new_top2:
        old_top2.delete(save=False)

    # Binge top 3
    try:
        old_top3 = StaticInfo.objects.get(pk=instance.pk).bingetop3image
    except StaticInfo.DoesNotExist:
        return False

    new_top3 = instance.bingetop3image
    if not old_top3 == new_top3:
        old_top3.delete(save=False)
