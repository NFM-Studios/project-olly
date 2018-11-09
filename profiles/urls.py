from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'profiles'

# profile/
urlpatterns = [
    url(r'^$', views.profile_no_username, name='profile_no_username'),
    url(r'^edit/$', login_required(views.edit_profile), name='edit_profile'),
    url(r'^users/$', views.users, name='users'),
    url(r'^users/search/$', login_required(views.searchusers), name='searchusers'),
    url(r'^user/(?P<urlusername>[A-Za-z0-9_@+.-]+)/$', views.profile, name='profile'),
    url(r'^leaderboards/$', views.LeaderboardView.as_view(), name='leaderboard'),
]
