from django.contrib.auth.decorators import login_required
from django.urls import path

from matches.views import *

app_name = 'matches'

urlpatterns = [
    path('', login_required(MatchList.as_view()), name='list'),
    path('<int:pk>/', login_required(TournamentMatchDetailView.as_view()), name='detail'),
    path('<int:pk>/report/', login_required(MatchReportCreateView.as_view()), name='report'),
    path('<int:pk>/dispute/', login_required(MatchDisputeReportCreateView.as_view()), name='dispute'),
    path('maps/<int:pk>/', login_required(MapPoolDetail.as_view()), name='maps_detail')

]
