from django.db import models
from django.dispatch import receiver


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
