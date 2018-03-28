from django.contrib import admin
from .models import Match, MatchReport, Ruleset

admin.site.register(Match, MatchReport, Ruleset)
