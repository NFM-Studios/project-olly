from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'profiles'

# profile/
urlpatterns = [
    path('', views.profile_no_username, name='profile_no_username'),
    path('edit/', login_required(views.edit_profile), name='edit_profile'),
    path('users/', views.users, name='users'),
    path('users/search/', login_required(views.searchusers), name='searchusers'),
    path('user/<str:urlusername>/', views.profile, name='profile'),
    path('leaderboards/', views.LeaderboardView.as_view(), name='leaderboard'),
]
