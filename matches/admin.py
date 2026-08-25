from django.contrib import admin

from .models import Match, MapChoice, MapPoolChoice, MatchCheckIn, GameChoice, PlatformChoice


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('type', 'hometeam', 'awayteam', 'completed', 'datetime')
    list_filter = ('type', 'completed', 'reported', 'disputed')
    search_fields = ('hometeam__name', 'awayteam__name', 'server')
    raw_id_fields = ('hometeam', 'awayteam', 'winner', 'loser', 'game', 'platform', 'map_pool')


admin.site.register(MapChoice)
admin.site.register(MapPoolChoice)
admin.site.register(MatchCheckIn)
admin.site.register(GameChoice)
admin.site.register(PlatformChoice)