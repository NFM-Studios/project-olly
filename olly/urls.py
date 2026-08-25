#from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from paypal.standard.ipn import views as paypal_views
from pages.models import StaticPage
from pages import views as pages_views
from profiles import views as profile_views

handler404 = pages_views.notfound

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', pages_views.index, name='index'),
    path('about/', pages_views.about, name='about'),
    path('terms/', pages_views.terms, name='terms'),
    path('partners/', pages_views.partners_page, name='partners'),
    path('sponsors/', pages_views.partners_page, name='partners'),
    path('privacy/', pages_views.privacy, name='privacy'),
    path('updates/', pages_views.whats_new, name='updates'),
    path('pages/<slug:slug>/', pages_views.static_page, name='static_page'),

    path('register/', profile_views.CreateUserFormView.as_view(), name='register'),
    path('login/', profile_views.LoginView.as_view(), name='login'),
    path('logout/', profile_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('reset-password/', profile_views.PasswordResetView.as_view(), name='reset_password'),
    path('reset-password/done/', profile_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    re_path(r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
            profile_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset-password/complete/', profile_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    re_path(r"^activate/(?P<uidb64>[0-9A-Za-z_'\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
            profile_views.activate, name='activate'),

    path('profile/', include('profiles.urls', namespace='profiles')),
    path('support/', include('support.urls', namespace='support')),
    path('teams/', include('teams.urls', namespace='teams')),
    path('news/', include('news.urls', namespace='news')),
    path('store/', include('store.urls', namespace='store')),
    path('paypal/', paypal_views.ipn, name="paypal-ipn"),
    path('staff/', include('staff.urls', namespace='staff')),
    path('tournaments/', include('singletournaments.urls', namespace='singletournaments')),
    path('matches/', include('matches.urls', namespace='matches')),
    path('wagers/', include('wagers.urls', namespace='wagers')),
    path('leagues/', include('leagues.urls', namespace='league')),

    path('api/', include('api.urls')),

    path('healthz/', pages_views.healthz, name='healthz'),
    path('readyz/', pages_views.readyz, name='readyz'),
]
#if settings.DEBUG is True:
 #   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
