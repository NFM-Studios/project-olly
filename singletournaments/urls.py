from django.contrib.auth.decorators import login_required
from django.urls import path

from singletournaments import views as tournament_views

app_name = 'singletournaments'

urlpatterns = [

    path('', tournament_views.List.as_view(), name='list'),
    path('<int:pk>/join/', login_required(tournament_views.SingleTournamentJoin.as_view()), name='join'),
    path('<int:pk>/', tournament_views.SingleTournamentDetail.as_view(), name='detail'),
    path('<int:pk>/rules/', login_required(tournament_views.SingleTournamentRules.as_view()), name='ruleset'),
    path('<int:pk>/bracket/', login_required(tournament_views.SingleTournamentBracket.as_view()), name='bracket'),
    path('<int:pk>/teams/', login_required(tournament_views.SingleTournamentTeamsList.as_view()), name='teams'),
    path('<int:pk>/matches/', login_required(tournament_views.SingleTournamentMatchList.as_view()), name='matches'),
    path('<int:pk>/leave/', login_required(tournament_views.SingleTournamentLeave.as_view()), name='leave'),

]
