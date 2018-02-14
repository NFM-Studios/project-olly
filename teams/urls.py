from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from teams.views import MyTeamListView, MyTeamDetailView, TeamCreateView

app_name = 'teams'

urlpatterns = [
    url(r'^my/$', login_required(MyTeamListView.as_view()), name='list'),
    url(r'^/(?P<pk>\d+)/$', login_required(MyTeamDetailView.as_view()), name='detail'),
    url(r'^create/$', login_required(TeamCreateView.as_view()), name='create'),
]
