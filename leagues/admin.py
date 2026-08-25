from django.contrib import admin
from .models import League, LeagueDivision, LeagueTeam, LeagueSettings


@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'active', 'game')
    list_filter = ('status', 'active', 'game')
    search_fields = ('name',)
    raw_id_fields = ('game', 'platform', 'sport', 'maps', 'settings', 'ruleset')


admin.site.register(LeagueDivision)
admin.site.register(LeagueTeam)
admin.site.register(LeagueSettings)