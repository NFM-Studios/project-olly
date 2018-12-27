from django.conf.urls import url, include
from django.urls import path
from django.contrib import admin
from profiles import views as profile_views
from pages import views as pages_views
from store import views as store_views
from support import views as support_views
from news import views as news_views
from teams import views as teams_views
from matches import views as matches_views
from django.contrib.auth.views import logout, password_reset, password_reset_done, password_reset_confirm,\
password_reset_complete
from django.conf import settings
from django.conf.urls.static import static
from paypal.standard.ipn import views as paypal_views

handler404 = pages_views.notfound

urlpatterns = [
    path('', pages_views.index, name='index'),
    path('about/', pages_views.about, name='about'),
    path('terms/', pages_views.terms, name='terms'),
    path('partners/', pages_views.partners_page, name='partners'),
    path('privacy/', pages_views.privacy, name='privacy'),
    path('404/', pages_views.notfound),
    path('register/', profile_views.CreateUserFormView.as_view(), name='register'),
    path('login/', profile_views.login, {'template_name': 'profiles/login_form.html'}, name='login'),
    path('logout/', profile_views.logout, name='logout'),
    path('reset-password/', profile_views.password_reset, name='reset_password'),
    path('reset-password/done/', profile_views.password_reset_done, name='password_reset_done'),
    url(r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', profile_views.password_reset_confirm, name='password_reset_confirm'),
    path('reset-password/complete/', profile_views.password_reset_complete, name='password_reset_complete'),
    path('admin/', admin.site.urls),
    path('profile/', include('profiles.urls', namespace='profiles')),
    path('support/', include('support.urls',namespace='support')),
    path('teams/', include('teams.urls',namespace='teams')),
    url(r"^activate/(?P<uidb64>[0-9A-Za-z_'\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
        profile_views.activate, name='activate'),
    path('news/', include('news.urls', namespace='news')),
    path('store/', include('store.urls', namespace='store')),
    path('paypal/', paypal_views.ipn, name="paypal-ipn"),
    url(r'^(?i)staff/', include('staff.urls', namespace='staff')),
    path('tournaments/', include('singletournaments.urls', namespace='singletournaments')),
    path('matches/', include('matches.urls', namespace='matches'))
]
if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
