from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from support.views import MyTicketListView, MyTicketDetailView, TicketCreateView

app_name = 'support'

urlpatterns = [
    url(r'^$', login_required(MyTicketListView.as_view()), name='list'),
    url(r'^my/(?P<pk>\d+)/$', login_required(MyTicketDetailView.as_view()), name='detail'),
    url(r'^create/$', login_required(TicketCreateView.as_view()), name='create'),
]
