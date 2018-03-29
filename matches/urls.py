from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'matches'

# profile/
urlpatterns = [
    url(r'^(?P<pk>\d+)/$', login_required(MatchDetailView.as_view()), name='detail'),
    url(r'^(?P<pk>\d+)/report$', login_required(MatchReportCreateView.as_view()), name='report'),

]
