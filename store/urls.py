from django.contrib.auth.decorators import login_required
from django.urls import path

from store import views as store_views

app_name = 'store'

urlpatterns = [

    path('', store_views.store, name='store'),
    path('product/<int:pk>/', login_required(store_views.detail), name='detail'),
    path('transfer/', login_required(store_views.Transfer.as_view()), name='transfer')
]