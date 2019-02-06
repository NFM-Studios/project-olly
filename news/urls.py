from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    # post views
    path('', views.post_list, name='post_list'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
]
