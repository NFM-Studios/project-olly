from django.contrib import admin

from profiles.models import UserProfile, Notification

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Notification)
