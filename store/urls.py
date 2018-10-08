from django.conf.urls import url, include
from store import views as store_views
from django.contrib.auth.decorators import login_required

app_name = 'store'

urlpatterns = [

    url(r'^$', store_views.store, name='store'),
    url(r'^product/(?P<pk>[0-9])/$', login_required(store_views.detail), name='detail'),
    url(r'^transfer/', login_required(store_views.Transfer.as_view()), name='transfer')
]