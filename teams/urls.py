from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from teams.views import MyTeamsListView, MyTeamDetailView, TeamCreateView, TeamInviteCreateView, CaptainInviteCreateView

app_name = 'teams'

urlpatterns = [
    url(r'^my/$', login_required(MyTeamsListView.as_view()), name='list'),
    url(r'^(?P<pk>\d+)/$', login_required(MyTeamDetailView.as_view()), name='detail'),
    url(r'^create/$', login_required(TeamCreateView.as_view()), name='create'),
    url(r'^invite/$', login_required(TeamInviteCreateView.as_view()), name='invite'),
    url(r'^captain/$', login_required(CaptainInviteCreateView.as_view()), name='captaininvite'),

]
