from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'staff'

urlpatterns = [
    url(r'^$', login_required(views.staffindex)),
    url(r'^users/$', login_required(views.users), name='users'),
    url(r'^tickets/$', login_required(views.tickets), name='tickets'),
    url(r'^ticketdetail/(?P<pk>\d+)/$', login_required(views.TicketDetail.as_view()), name='ticket_detail'),
    url(r'^ticketcomment/(?P<pk>\d+)/$', login_required(views.TicketCommentCreate.as_view()), name='ticket_comment_create'),
    url(r'^staticinfo/$', login_required(views.staticinfo), name='staticinfo'),
    url(r'^users/ban/(?P<urlusername>\w+)/$', login_required(views.banuser)),
    url(r'^users/unban/(?P<urlusername>\w+)/$', login_required(views.unbanuser)),
    url(r'^users/banip/(?P<urlusername>\w+)/$', login_required(views.banip)),
    url(r'^users/unbanip/(?P<urlusername>\w+)/$', login_required(views.unbanip)),
    url(r'^users/search/$', login_required(views.searchusers), name='searchusers'),
    url(r'^users/edit/(?P<urlusername>\w+)/$', login_required(views.edituser)),
    url(r'^tournaments/$', login_required(views.tournaments), name='tournamentlist'),
    url(r'^tournaments/edit/(?P<pk>\d+)/$', login_required(views.edit_tournament), name='edit_tournament'),
    url(r'^tournaments/create$', login_required(views.CreateTournament.as_view()), name='create_tournament'),
    url(r'^news/', login_required(views.news_index), name='news_index'),
    url(r'^news/list', login_required(views.news_list), name='news_list'),
    url(r'^news/create', login_required(views.create_article), name='create_article'),
]
