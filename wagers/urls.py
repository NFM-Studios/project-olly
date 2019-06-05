from django.contrib.auth.decorators import login_required
from django.urls import path

from wagers.views import *

app_name = 'wagers'

urlpatterns = [
    path('', login_required(WagerRequestList.as_view()), name='list'),
    path('<int:pk>/challenge/', login_required(WagerChallengeCreate.as_view()), name='challenge_create'),
    path('<int:pk>/', login_required(WagerRequestDetail.as_view()), name='request_detail'),
    path('<int:pk>/delete', login_required(WagerRequestDeleteView.as_view()), name='request_delete'),
    path('request', login_required(WagerRequestCreateView.as_view()), name='request_create'),
    path('<int:pk>/match', login_required(WagerMatchDetail.as_view()), name='match_detail'),
    #path('my', )
]
