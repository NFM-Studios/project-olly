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
    url(r'^user/(?P<urlusername>\w+)/$', views.profile, name='profile'),
    url(r'^leaderboards/$', login_required(views.LeaderboardView.as_view()), name='leaderboard'),
]
