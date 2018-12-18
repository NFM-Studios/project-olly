from django.conf.urls import url
from . import views

app_name = 'news'

urlpatterns = [
    # post views
    url(r'^$', views.post_list, name='post_list'),
    url(r'^(?P<slug>[A-Za-z0-9_@+.-]+)/$', views.post_detail, name='post_detail'),
    url(r'^(?P<post_id>\d+)/share/$', views.post_share, name='post_share'),
]
