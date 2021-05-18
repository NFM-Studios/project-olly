from django.db import models


class UserBanRecord(models.Model):
    profile = models.ForeignKey('profiles.UserProfile', related_name='banned_profile', on_delete=models.SET_NULL, null=True)
    reason = models.TextField(default="Not specified")
    admin = models.ForeignKey('profiles.UserProfile', related_name='ban_admin', on_delete=models.SET_NULL, null=True)
    datetime = models.DateTimeField(auto_created=True)


class UserUnbanRecord(models.Model):
    profile = models.ForeignKey('profiles.UserProfile', related_name='unbanned_profile', on_delete=models.SET_NULL,
                                null=True)
    reason = models.TextField(default="Not specified")
    admin = models.ForeignKey('profiles.UserProfile', related_name='unban_admin', on_delete=models.SET_NULL, null=True)
    datetime = models.DateTimeField(auto_created=True)
