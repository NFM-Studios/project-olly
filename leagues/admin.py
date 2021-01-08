from django.contrib import admin
from .models import League, LeagueDivision, LeagueTeam, LeagueSettings

admin.site.register(League)
admin.site.register(LeagueDivision)
admin.site.register(LeagueTeam)
admin.site.register(LeagueSettings)
