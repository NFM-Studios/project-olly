from django.db import models
from django.dispatch import receiver


class StaticInfo(models.Model):
    about_us = models.TextField(default='about us')
    terms = models.TextField(default='terms of service')
    #privacy = models.TextField(default='privacy policy')
    stream = models.CharField(default='twitch', max_length=25)
    slide1link = models.TextField(default="#")
    slide2link = models.TextField(default="#")
    slide3link = models.TextField(default="#")
    slide1_img = models.ImageField(upload_to='carousel_images', blank=True)
    slide2_img = models.ImageField(upload_to='carousel_images', blank=True)
    slide3_img = models.ImageField(upload_to='carousel_images', blank=True)
    welcomeln1 = models.CharField(default='welcome1', max_length=25)
    welcomeln2 = models.CharField(default='welcome2', max_length=25)

    bingeslide1big = models.TextField(default="Coming Soon!")
    bingeslide1small = models.TextField(default="Coming Soon!")
    bingeslide1link = models.URLField(max_length=200, default="#")
    # bingeslide1image =

    bingeslide2big = models.TextField(default="Coming Soon!")
    bingeslide2small = models.TextField(default="Coming Soon!")
    bingeslide2link = models.URLField(max_length=200, default='#')
    # bingeslide2image

    bingeslide3big = models.TextField(default="Coming Soon!")
    bingeslide3small = models.TextField(default="Coming Soon!")
    bingeslide3link = models.URLField(max_length=200, default="#")
    # bingeslide3image

    bingetop1 = models.TextField(default="Coming Soon!")
    #bingetop1image =
    bingetop1link = models.URLField(max_length=200, default="#")


    bingetop2 = models.TextField(default="Coming Soon!")
    #bingetop2image =
    bingetop2link = models.URLField(max_length=200, default="#")


    bingetop3 = models.TextField(default="Coming Soon!")
    #bingetop3image =
    bingetop3link = models.URLField(max_length=200, default="#")



    # for steven

    # slide1_pic
    # slide2_pic
    # slide3_pic


class Partner(models.Model):
    name = models.CharField(max_length=80)
    website = models.URLField(default="#", blank=True)
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
