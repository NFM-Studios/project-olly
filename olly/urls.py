from django.conf.urls import url, include
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


urlpatterns = [
    url(r'^$', pages_views.index, name='index'),
    url(r'^about/', pages_views.about, name='about'),
    url(r'^terms/', pages_views.terms, name='terms'),
    url(r'^privacy/', pages_views.privacy, name='privacy'),
    url(r'^404/', pages_views.notfound),
    url(r'^register/', profile_views.CreateUserFormView.as_view(), name='register'),
    url(r'^login/', profile_views.login, {'template_name': 'profiles/login_form.html'}, name='login'),
    url(r'^logout/', logout, {'template_name': 'index.html', 'next_page': '/'}, name='logout'),
    url(r'^reset-password/$', password_reset, {'template_name': 'profiles/reset_form.html', 'email_template_name':
        'profiles/reset_email.html'}, name='reset_password'),
    url(r'^reset-password/done/$', password_reset_done, {'template_name': 'profiles/reset_done.html'},
        name='password_reset_done'),
    url(r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm,
        {'template_name': 'profiles/reset_confirm.html'}, name='password_reset_confirm'),
    url(r'^reset-password/complete$', password_reset_complete, {'template_name': 'profiles/reset_complete.html'},
        name='password_reset_complete'),
    url(r'^admin/', admin.site.urls),
    url(r'^profile/', include('profiles.urls', namespace='profiles')),
    url(r'^support/', include('support.urls',namespace='support')),
    url(r'^teams/', include('teams.urls',namespace='teams')),
    url(r"^activate/(?P<uidb64>[0-9A-Za-z_'\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
        profile_views.activate, name='activate'),
    url(r'^news/', include('news.urls', namespace='news')),
    url(r'^store/', include('store.urls', namespace='store')),
    url(r'^paypal/', paypal_views.ipn, name="paypal-ipn"),
    url(r'^staff/', include('staff.urls', namespace='staff')),
    url(r'^tournaments/', include('singletournaments.urls', namespace='singletournaments')),
    url(r'^matches/', include('matches.urls', namespace='matches'))
]
if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
