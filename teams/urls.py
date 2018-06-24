from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required
from teams.views import MyTeamsListView, MyTeamDetailView, TeamCreateView, TeamInviteCreateView, MyInvitesListView, InviteView

app_name = 'teams'

urlpatterns = [
    url(r'^$', login_required(MyTeamsListView.as_view()), name='list'),
    url(r'^invites/$', login_required(MyInvitesListView.as_view()), name='myinvitelist'),
    url(r'^invites/(?P<num>[0-9]*)/$', login_required(InviteView)),
    url(r'^(?P<pk>\d+)/$', MyTeamDetailView.as_view(), name='detail'),
    url(r'^create/$', login_required(TeamCreateView.as_view()), name='create'),
    url(r'^invite/$', login_required(TeamInviteCreateView.as_view()), name='invite'),
    url(r'^(?P<pk>\d+)/edit/$', login_required(views.EditTeamView), name='edit'),
    url(r'^(?P<pk>\d+)/leave/$', login_required(views.LeaveTeamView.as_view()), name='leave'),
    url(r'^(?P<pk>\d+)/remove/$', login_required(views.RemoveUserView.as_view()), name='remove'),

]
