from django.contrib import admin

from profiles.models import UserProfile, Notification


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'xp', 'country', 'rank')
    search_fields = ('user__username', 'user__email', 'alternate_name', 'discord', 'steamid64')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'sender', 'datetime', 'read', 'seen')
    list_filter = ('type', 'read', 'seen')
    search_fields = ('title', 'description', 'sender')