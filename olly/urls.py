from django.conf.urls import url, include
from django.contrib import admin
from profiles import views as profile_views
from pages import views as pages_views
from django.contrib.auth.views import login
from django.contrib.auth.views import logout
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', pages_views.index),#replace with pages app eventually
    url(r'^about/', pages_views.about),
    url(r'^terms/', pages_views.terms),
    url(r'^privacy/', pages_views.privacy),
    url(r'^404/', pages_views.notfound),
    url(r'^news/', include('news.urls')),
    url(r'^register/', profile_views.CreateUserFormView.as_view(), name='register'),
    url(r'^login/', login, {'template_name': 'profiles/login_form.html'}, name='login'),
    url(r'^logout/', logout, {'template_name': 'index.html', 'next_page': '/'}, name='logout'),
    url(r'^admin/', admin.site.urls),
    url(r'^profile/', include('profiles.urls', namespace='profiles')),
    url(r"^activate/(?P<uidb64>[0-9A-Za-z_'\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
        profile_views.activate, name='activate'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
