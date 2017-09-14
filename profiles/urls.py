from django.conf.urls import url
from . import views

# profile/
urlpatterns = [
    url(r'^$', views.profile_no_username, name='profile_no_username'),
    url(r'^edit/$', views.edit_profile, name='edit_profile'),
    url(r'^user/(?P<urlusername>\w+)/$', views.profile, name='profile'),
]
