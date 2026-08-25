from django.contrib import admin

from .models import Team, TeamInvite


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'tag', 'founder', 'rank')
    search_fields = ('name', 'tag', 'founder__username')
    raw_id_fields = ('founder',)


admin.site.register(TeamInvite)