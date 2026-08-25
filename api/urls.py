from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONOpenAPIRenderer
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view

from api import views

router = DefaultRouter()
router.register(r'teams', views.TeamViewSet, basename='team')
router.register(r'matches', views.MatchViewSet, basename='match')
router.register(r'tournaments', views.TournamentViewSet, basename='tournament')
router.register(r'leagues', views.LeagueViewSet, basename='league')
router.register(r'news/posts', views.PostViewSet, basename='post')
router.register(r'games', views.GameViewSet, basename='game')
router.register(r'platforms', views.PlatformViewSet, basename='platform')
router.register(r'map-pools', views.MapPoolViewSet, basename='mappool')
router.register(r'wagers/requests', views.WagerRequestViewSet, basename='wagerrequest')

schema_view = get_schema_view(
    title='Project-Olly API',
    description='REST API for the Project-Olly esports platform.',
    version='1.0.0',
    public=True,
    permission_classes=[AllowAny],
    renderer_classes=[JSONOpenAPIRenderer],
)

urlpatterns = [
    path('me/', views.MeView.as_view(), name='me'),
    path('me/notifications/', views.NotificationsView.as_view(), name='me-notifications'),
    path('docs/', schema_view, name='docs'),
]

urlpatterns += router.urls