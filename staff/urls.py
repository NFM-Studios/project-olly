from django.conf.urls import url
from . import views

app_name = 'staff'

urlpatterns = [
    url(r'^$', views.staffindex),
    url(r'^users/$', views.users),
    url(r'^tickets/$', views.tickets),
    url(r'^staticinfo/$', views.staticinfo, name='staticinfo'),
    url(r'^users/ban/(?P<urlusername>\w+)/$', views.banuser),
    url(r'^users/unban/(?P<urlusername>\w+)/$', views.unbanuser),
    url(r'^users/banip/(?P<urlusername>\w+)/$', views.banip),
    url(r'^users/unbanip/(?P<urlusername>\w+)/$', views.unbanip),
    url(r'^users/search/$', views.searchusers, name='searchusers'),
    url(r'^users/edit/(?P<urlusername>\w+)/$', views.edituser)
]
