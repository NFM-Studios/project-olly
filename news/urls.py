from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    # post views
    path('', views.post_list, name='post_list'),
    url(r'^(?P<slug>[A-Za-z0-9_@+.-]+)/$', views.post_detail, name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
]
