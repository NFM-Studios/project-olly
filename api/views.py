import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from api.permissions import IsMatchParticipantOrStaff, IsStaffOrReadOnly, IsTeamOwnerOrStaff
from api.serializers import (
    CommentSerializer,
    GameSerializer,
    LeagueSerializer,
    MapPoolSerializer,
    MatchSerializer,
    MeSerializer,
    NotificationSerializer,
    OwnProfileUpdateSerializer,
    PlatformSerializer,
    PostSerializer,
    TournamentRoundSerializer,
    TournamentSerializer,
    TeamSerializer,
    UserSerializer,
    WagerRequestSerializer,
)
from leagues.models import League
from matches.models import GameChoice, MapPoolChoice, Match, PlatformChoice
from news.models import Post
from profiles.models import Notification, UserProfile
from singletournaments.models import SingleEliminationTournament, SingleTournamentRound
from staff.views import is_staff_user
from teams.models import Team
from wagers.models import WagerRequest


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class TeamFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Team
        fields = ['name', 'country']


class MatchFilter(django_filters.FilterSet):
    class Meta:
        model = Match
        fields = {
            'game': ['exact'],
            'platform': ['exact'],
            'hometeam': ['exact'],
            'awayteam': ['exact'],
            'completed': ['exact'],
            'datetime': ['exact', 'gte', 'lte'],
        }


class TournamentFilter(django_filters.FilterSet):
    class Meta:
        model = SingleEliminationTournament
        fields = {
            'active': ['exact'],
            'game': ['exact'],
            'platform': ['exact'],
        }


class LeagueFilter(django_filters.FilterSet):
    class Meta:
        model = League
        fields = {
            'active': ['exact'],
            'game': ['exact'],
            'platform': ['exact'],
        }


class PostFilter(django_filters.FilterSet):
    class Meta:
        model = Post
        fields = {
            'status': ['exact'],
            'author': ['exact'],
        }


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    filterset_class = TeamFilter
    pagination_class = StandardResultsSetPagination
    ordering_fields = ['name', 'created', 'updated', 'rank', 'totalxp']
    ordering = ['-updated']

    def get_queryset(self):
        return Team.objects.all().prefetch_related('captain', 'players')

    def perform_create(self, serializer):
        team = serializer.save(founder=self.request.user)
        profile = UserProfile.objects.get(user=self.request.user)
        profile.founder_teams.add(team)

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'destroy'):
            return [permissions.IsAuthenticatedOrReadOnly(), IsTeamOwnerOrStaff()]
        return [permissions.IsAuthenticatedOrReadOnly()]

    @action(detail=True, methods=['get'], url_path='players')
    def players(self, request, pk=None):
        team = self.get_object()
        serializer = UserSerializer(team.players.all(), many=True,
                                    context={'request': request})
        return Response(serializer.data)


class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    filterset_class = MatchFilter
    pagination_class = StandardResultsSetPagination
    ordering_fields = ['datetime', 'matchnum']
    ordering = ['-datetime']

    def get_queryset(self):
        return Match.objects.all().select_related(
            'hometeam', 'awayteam', 'winner', 'loser', 'game', 'platform',
            'sport', 'map_pool').prefetch_related('maps')

    def get_permissions(self):
        if self.action in ('create', 'destroy'):
            return [IsStaffOrReadOnly()]
        return [permissions.IsAuthenticatedOrReadOnly(), IsMatchParticipantOrStaff()]


class TournamentViewSet(viewsets.ModelViewSet):
    queryset = SingleEliminationTournament.objects.all()
    serializer_class = TournamentSerializer
    filterset_class = TournamentFilter
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsStaffOrReadOnly]
    ordering_fields = ['name', 'start']
    ordering = ['-start']

    def get_queryset(self):
        return SingleEliminationTournament.objects.all().prefetch_related(
            'teams', 'winner', 'second', 'third')

    @action(detail=True, methods=['get'], url_path='rounds')
    def rounds(self, request, pk=None):
        tournament = self.get_object()
        rounds_qs = SingleTournamentRound.objects.filter(
            tournament=tournament).order_by('roundnum').prefetch_related(
            'matches__hometeam', 'matches__awayteam')
        serializer = TournamentRoundSerializer(rounds_qs, many=True,
                                               context={'request': request})
        return Response(serializer.data)


class LeagueViewSet(viewsets.ModelViewSet):
    queryset = League.objects.all()
    serializer_class = LeagueSerializer
    filterset_class = LeagueFilter
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsStaffOrReadOnly]
    ordering_fields = ['name', 'start']
    ordering = ['-start']

    def get_queryset(self):
        return League.objects.all().prefetch_related('teams__team')


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    filterset_class = PostFilter
    pagination_class = StandardResultsSetPagination
    ordering_fields = ['publish', 'created']
    ordering = ['-publish']

    def get_queryset(self):
        if is_staff_user(self.request.user):
            return Post.objects.all()
        return Post.objects.filter(status='published')

    def get_permissions(self):
        if self.action == 'comments' and self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [IsStaffOrReadOnly()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['get', 'post'], url_path='comments')
    def comments(self, request, pk=None):
        post = self.get_object()
        if request.method == 'GET':
            serializer = CommentSerializer(post.comments.filter(active=True),
                                           many=True)
            return Response(serializer.data)
        serializer = CommentSerializer(data=request.data,
                                       context={'request': request})
        if serializer.is_valid():
            serializer.save(post=post)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class GameViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GameChoice.objects.all()
    pagination_class = StandardResultsSetPagination
    serializer_class = GameSerializer


class PlatformViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PlatformChoice.objects.all()
    pagination_class = StandardResultsSetPagination
    serializer_class = PlatformSerializer


class MapPoolViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MapPoolChoice.objects.all()
    pagination_class = StandardResultsSetPagination
    serializer_class = MapPoolSerializer

    def get_queryset(self):
        return MapPoolChoice.objects.all().prefetch_related('maps')


class WagerRequestViewSet(viewsets.ModelViewSet):
    queryset = WagerRequest.objects.all()
    pagination_class = StandardResultsSetPagination
    serializer_class = WagerRequestSerializer
    ordering_fields = ['posted']
    ordering = ['-posted']

    def get_queryset(self):
        return WagerRequest.objects.all().select_related('team', 'game', 'platform')

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]


class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def _fresh_user(request):
        from django.contrib.auth.models import User
        return User.objects.select_related('user').get(pk=request.user.pk)

    def get(self, request):
        serializer = MeSerializer(self._fresh_user(request))
        return Response(serializer.data)

    def patch(self, request):
        user = self._fresh_user(request)
        profile = user.user
        serializer = OwnProfileUpdateSerializer(profile, data=request.data,
                                                partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(MeSerializer(self._fresh_user(request)).data)
        return Response(serializer.errors, status=400)


class NotificationsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def _profile(self, request):
        return MeView._fresh_user(request).user

    def get(self, request):
        queryset = self._profile(request).notifications.all().order_by('-datetime', '-id')
        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = NotificationSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        ids = request.data.get('ids')
        if ids is None:
            single_id = request.data.get('id')
            if single_id is None:
                return Response(
                    {'detail': 'Provide an "id" (or "ids") of a notification to '
                               'mark as read.'}, status=400)
            ids = [single_id]
        owned = self._profile(request).notifications.all()
        for notif_id in ids:
            try:
                notification = owned.get(id=notif_id)
            except Notification.DoesNotExist:
                return Response({'detail': 'Notification not found.'}, status=404)
            if not notification.read:
                notification.read = True
                notification.save(update_fields=['read'])
        return Response({'detail': 'Notification(s) marked as read.'})