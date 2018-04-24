from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from matches.views import TournamentMatchDetailView, MatchReportCreateView, MatchDisputeReportCreateView

app_name = 'matches'


urlpatterns = [
    url(r'^(?P<pk>\d+)/$', login_required(TournamentMatchDetailView.as_view()), name='detail'),
    url(r'^(?P<pk>\d+)/report$', login_required(MatchReportCreateView.as_view()), name='report'),
    url(r'^(?P<pk>\d+)/dispute', login_required(MatchDisputeReportCreateView.as_view()), name='dispute'),


]
