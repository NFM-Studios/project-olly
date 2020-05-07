from django.contrib.auth.decorators import login_required
from django.urls import path

from support.views import MyTicketListView, MyTicketDetailView, TicketCreateView, FAQDetail, FAQListView

app_name = 'support'

urlpatterns = [
    path('', login_required(MyTicketListView.as_view()), name='list'),
    path('my/<int:pk>/', login_required(MyTicketDetailView.as_view()), name='detail'),
    path('create/', login_required(TicketCreateView.as_view()), name='create'),
    path('faq/', FAQListView, name='faq_list'),
    path('faq/<int:pk>/', FAQDetail, name='faq_detail')
]
