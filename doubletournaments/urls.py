from django.contrib.auth.decorators import login_required
from django.urls import path

from doubletournaments import views as tournament_views

app_name = 'doubletournaments'

urlpatterns = [
    path('', tournament_views.List.as_view(), name='list'),
    path('<int:pk>/', tournament_views.DoubleEliminationTournamentDetail.as_view(), name='detail'),
    path('<int:pk>/join/', login_required(tournament_views.DoubleEliminationTournamentJoin.as_view()),
         name='join'),
    path('<int:pk>/leave/', login_required(tournament_views.DoubleEliminationTournamentLeave.as_view()),
         name='leave'),
    path('<int:pk>/bracket/', tournament_views.DoubleEliminationTournamentBracket.as_view(), name='bracket'),
    path('<int:pk>/teams/', tournament_views.DoubleEliminationTournamentTeamsList.as_view(), name='teams'),
    path('ruleset/<int:pk>/', tournament_views.RulesetDetail.as_view(), name='ruleset'),
]