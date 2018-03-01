from django.conf.urls import url, include
from store import views as store_views
from django.contrib.auth.decorators import login_required

app_name = 'store'

urlpatterns = [

    url(r'^$', login_required(store_views.store), name='store'),
    url(r'^product/(?P<num>[0-9])/$', login_required(store_views.buy_credits)),
    url(r'^transfer/', login_required(store_views.Transfer.as_view()))
]