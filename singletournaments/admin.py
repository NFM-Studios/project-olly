from django.contrib import admin
from .models import SingleTournamentTeam, SingleEliminationTournament, SingleTournamentRound

admin.site.register(SingleEliminationTournament, SingleTournamentRound, SingleTournamentTeam)
