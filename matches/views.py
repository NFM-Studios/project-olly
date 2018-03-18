from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from singletournaments.models import SingleEliminationTournament
from teams.models import Team
from matches.models import Match


class TournamentMatchDetailView(DetailView):
    model = Match

