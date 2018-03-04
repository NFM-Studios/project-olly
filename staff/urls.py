from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'staff'

urlpatterns = [
    url(r'^$', login_required(views.staffindex)),
    url(r'^users/$', login_required(views.users), name='users'),
    url(r'^tickets/$', login_required(views.tickets), name='tickets'),
    url(r'^ticketdetail/(?P<pk>\d+)/$', login_required(views.TicketDetail.as_view()), name='ticket_detail'),
    url(r'^staticinfo/$', login_required(views.staticinfo), name='staticinfo'),
    url(r'^users/ban/(?P<urlusername>\w+)/$', login_required(views.banuser)),
    url(r'^users/unban/(?P<urlusername>\w+)/$', login_required(views.unbanuser)),
    url(r'^users/banip/(?P<urlusername>\w+)/$', login_required(views.banip)),
    url(r'^users/unbanip/(?P<urlusername>\w+)/$', login_required(views.unbanip)),
    url(r'^users/search/$', login_required(views.searchusers), name='searchusers'),
    url(r'^users/edit/(?P<urlusername>\w+)/$', login_required(views.edituser))
]
