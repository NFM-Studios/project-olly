from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required
from singletournaments import views as tournament_views

app_name = 'singletournaments'

urlpatterns = [

    url(r'^$', login_required(tournament_views.List.as_view()), name='list'),
    url(r'^join/$', login_required(tournament_views.SingleTournamentJoin.as_view()))

]