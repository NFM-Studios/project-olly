from django.contrib import admin

from .models import SingleEliminationTournament, SingleTournamentRound, SingleTournamentRuleset, SingleTournamentTeam

admin.site.register(SingleEliminationTournament)
admin.site.register(SingleTournamentRound)
admin.site.register(SingleTournamentRuleset)
admin.site.register(SingleTournamentTeam)
