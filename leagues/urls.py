from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views as views

app_name = 'leagues'

urlpatterns = [
    path('', login_required(views.list_leagues), name='list'),
    path('<int:pk>/', login_required(views.detail_league), name='detail'),
    path('<int:pk>/teams/', login_required(views.detail_league_teams), name='teams'),
    path('<int:pk>/divisions/', login_required(views.detail_league_divisions), name='divisions'),
    path('<int:pk>/rules/', login_required(views.detail_league_rules), name='rules'),
    path('<int:pk>/join/', login_required(views.join_league), name='join'),
    path('<int:pk>/leave/', login_required(views.leave_league), name='leave'),
]
