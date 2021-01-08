from django.contrib import admin

from .models import Match, MapChoice, MapPoolChoice, MatchCheckIn

admin.site.register(Match)
admin.site.register(MapChoice)
admin.site.register(MapPoolChoice)
admin.site.register(MatchCheckIn)
