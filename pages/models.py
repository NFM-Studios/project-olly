from django.db import models

# Create your models here.

class StaticInfo(models.Model):
    about_us = models.TextField(default = 'about us')
    terms = models.TextField(default = 'terms of service')
    privacy = models.TextField(default = 'privacy policy')
