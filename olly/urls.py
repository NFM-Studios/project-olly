from django.conf.urls import url, include
from django.contrib import admin
from profiles import views as profile_views
from pages import views as pages_views
from django.contrib.auth.views import login
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', profile_views.index),#replace with pages app eventually
    url(r'^pages/', pages_views.index),
    url(r'^news/', include('news.urls')),
    url(r'^register/', profile_views.CreateUserFormView.as_view(), name='register'),
    url(r'^login/', login, {'template_name': 'profiles/login_form.html'}, name='login'),
    url(r'^admin/', admin.site.urls),
    url(r'^profile/', include('profiles.urls', namespace='profiles'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
