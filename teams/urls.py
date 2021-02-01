from django.contrib.auth.decorators import login_required
from django.urls import path

from teams.views import MyTeamsListView, MyTeamDetailView, TeamCreateView, TeamInviteCreateView, MyInvitesListView, \
    invite_view, add_founder_as_captain
from . import views

app_name = 'teams'

urlpatterns = [
    path('', login_required(MyTeamsListView), name='list'),
    path('invites/', login_required(MyInvitesListView.as_view()), name='myinvitelist'),
    path('invites/<int:num>/', login_required(invite_view), name='invite_detail'),
    path('<int:pk>/', MyTeamDetailView.as_view(), name='detail'),
    path('create/', login_required(TeamCreateView.as_view()), name='create'),
    path('invite/', login_required(TeamInviteCreateView.as_view()), name='invite'),
    path('<int:pk>/edit/', login_required(views.edit_team_view), name='edit'),
    path('<int:pk>/leave/', login_required(views.LeaveTeamView.as_view()), name='leave'),
    path('<int:pk>/remove/', login_required(views.RemoveUserView.as_view()), name='remove'),
    path('<int:pk>/dissolve/', login_required(views.DissolveTeamView.as_view()), name='dissolve'),
    path('<int:pk>/founder-captain/', login_required(add_founder_as_captain), name='founder_captain')

]
