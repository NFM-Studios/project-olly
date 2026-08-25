from django.contrib.auth.models import User
from django_countries.serializer_fields import CountryField
from rest_framework import serializers
from rest_framework.relations import PKOnlyObject

from leagues.models import League, LeagueTeam
from matches.models import GameChoice, MapChoice, MapPoolChoice, Match, PlatformChoice, SportChoice
from news.models import Comment, Post
from profiles.models import Notification, UserProfile
from singletournaments.models import SingleEliminationTournament, SingleTournamentRound
from teams.models import Team
from wagers.models import WagerRequest


class UserProfilePublicSerializer(serializers.ModelSerializer):
    """Public profile fields - never expose email, ip, credits or earnings."""

    country = CountryField()

    class Meta:
        model = UserProfile
        fields = ['alternate_name', 'xp', 'about_me', 'steamid64', 'discord', 'xbl',
                  'psn', 'steam', 'epic', 'lol', 'battlenet', 'activisionid',
                  'twitch_channel', 'favorite_game', 'favorite_console',
                  'profile_picture', 'country', 'user_verified']


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfilePublicSerializer(source='user', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'profile']


class TeamSummarySerializer(serializers.ModelSerializer):
    country = CountryField()

    class Meta:
        model = Team
        fields = ['id', 'name', 'tag', 'country', 'image', 'rank', 'totalxp']


class TeamSerializer(serializers.ModelSerializer):
    founder = UserSerializer(read_only=True)
    captain = UserSerializer(many=True, read_only=True)
    players = UserSerializer(many=True, read_only=True)
    country = CountryField(required=False, allow_blank=True)

    class Meta:
        model = Team
        fields = ['id', 'name', 'tag', 'about_us', 'website', 'twitter', 'twitch',
                  'founder', 'captain', 'players', 'created', 'updated',
                  'num_matchwin', 'num_matchloss', 'country', 'image', 'rank',
                  'totalxp']
        read_only_fields = ['created', 'updated', 'num_matchwin', 'num_matchloss',
                            'rank', 'totalxp']

    def validate_name(self, value):
        if len(value) < 5:
            raise serializers.ValidationError(
                'Team name must be at least 5 characters long.')
        return value


class TeamPrimaryKeyNestedField(serializers.PrimaryKeyRelatedField):
    """Accept a team PK on write, serialize a nested team summary on read."""

    def to_representation(self, value):
        if isinstance(value, PKOnlyObject):
            value = self.get_queryset().get(pk=value.pk)
        return TeamSummarySerializer(value).data


class MatchSerializer(serializers.ModelSerializer):
    hometeam = TeamPrimaryKeyNestedField(queryset=Team.objects.all(),
                                         required=False, allow_null=True)
    awayteam = TeamPrimaryKeyNestedField(queryset=Team.objects.all(),
                                         required=False, allow_null=True)
    winner = TeamSummarySerializer(read_only=True)
    loser = TeamSummarySerializer(read_only=True)
    game = serializers.PrimaryKeyRelatedField(queryset=GameChoice.objects.all(),
                                              required=False, allow_null=True)
    platform = serializers.PrimaryKeyRelatedField(queryset=PlatformChoice.objects.all(),
                                                  required=False, allow_null=True)
    sport = serializers.PrimaryKeyRelatedField(queryset=SportChoice.objects.all(),
                                               required=False, allow_null=True)
    map_pool = serializers.PrimaryKeyRelatedField(queryset=MapPoolChoice.objects.all(),
                                                  required=False, allow_null=True)
    maps = serializers.PrimaryKeyRelatedField(many=True,
                                              queryset=MapChoice.objects.all(),
                                              required=False)

    class Meta:
        model = Match
        fields = ['id', 'type', 'matchnum', 'map_pool', 'maps', 'game', 'platform',
                  'sport', 'hometeam', 'awayteam', 'reported', 'completed',
                  'winner', 'loser', 'bestof', 'teamformat', 'team1reported',
                  'team2reported', 'server', 'datetime', 'info', 'disputed',
                  'disable_userreport', 'conference_match']
        read_only_fields = ['reported', 'completed', 'winner', 'loser',
                            'team1reported', 'team2reported', 'disputed',
                            'disable_userreport']


class TournamentSerializer(serializers.ModelSerializer):
    teams = TeamSummarySerializer(many=True, read_only=True)
    winner = TeamSummarySerializer(read_only=True)
    second = TeamSummarySerializer(read_only=True)
    third = TeamSummarySerializer(read_only=True)
    game = serializers.PrimaryKeyRelatedField(queryset=GameChoice.objects.all(),
                                              required=False, allow_null=True)
    platform = serializers.PrimaryKeyRelatedField(queryset=PlatformChoice.objects.all(),
                                                  required=False, allow_null=True)
    sport = serializers.PrimaryKeyRelatedField(queryset=SportChoice.objects.all(),
                                               required=False, allow_null=True)

    class Meta:
        model = SingleEliminationTournament
        fields = ['id', 'name', 'teamformat', 'bestof', 'active', 'twitch',
                  'open_register', 'close_register', 'allow_register', 'info',
                  'ruleset', 'created', 'updated', 'req_credits', 'platform',
                  'game', 'sport', 'start', 'teams', 'current_round', 'winner',
                  'second', 'third', 'size', 'bracket_generated', 'prize1',
                  'prize2', 'prize3', 'image', 'disable_userreport']
        read_only_fields = ['created', 'updated', 'current_round',
                            'bracket_generated', 'winner', 'second', 'third']


class TournamentRoundSerializer(serializers.ModelSerializer):
    matches = MatchSerializer(many=True, read_only=True)

    class Meta:
        model = SingleTournamentRound
        fields = ['id', 'roundnum', 'matchesnum', 'matches', 'info']


class LeagueTeamSerializer(serializers.ModelSerializer):
    team = TeamSummarySerializer(read_only=True)

    class Meta:
        model = LeagueTeam
        fields = ['id', 'team', 'wins', 'losses', 'ot_losses', 'ot_wins', 'ties',
                  'points']


class LeagueSerializer(serializers.ModelSerializer):
    standings = LeagueTeamSerializer(many=True, read_only=True, source='teams')
    game = serializers.PrimaryKeyRelatedField(queryset=GameChoice.objects.all(),
                                              required=False, allow_null=True)
    platform = serializers.PrimaryKeyRelatedField(queryset=PlatformChoice.objects.all(),
                                                  required=False, allow_null=True)
    sport = serializers.PrimaryKeyRelatedField(queryset=SportChoice.objects.all(),
                                               required=False, allow_null=True)

    class Meta:
        model = League
        fields = ['id', 'name', 'status', 'active', 'info', 'created', 'updated',
                  'platform', 'game', 'sport', 'teamformat', 'bestof',
                  'open_register', 'close_register', 'start', 'req_credits',
                  'size', 'disable_userreport', 'prize1', 'prize2', 'prize3',
                  'standings']
        read_only_fields = ['created', 'updated']


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'author', 'body', 'publish', 'created',
                  'updated', 'status', 'image']
        read_only_fields = ['author', 'created', 'updated']


class CommentSerializer(serializers.ModelSerializer):
    """Comments never expose the submitter's email address."""

    class Meta:
        model = Comment
        fields = ['id', 'post', 'name', 'body', 'created', 'updated', 'active']
        read_only_fields = ['post', 'created', 'updated', 'active']

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['email'] = request.user.email or 'noemail@example.com'
        validated_data.setdefault('name', request.user.username)
        return super().create(validated_data)


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameChoice
        fields = ['id', 'name', 'image']


class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlatformChoice
        fields = ['id', 'name', 'image']


class MapChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapChoice
        fields = ['id', 'name', 'map_num', 'game']


class MapPoolSerializer(serializers.ModelSerializer):
    maps = MapChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = MapPoolChoice
        fields = ['id', 'name', 'maps', 'description', 'game']


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'title', 'description', 'sender', 'type', 'datetime',
                  'link', 'read', 'seen']


class OwnProfileSerializer(serializers.ModelSerializer):
    """Full profile for /api/me/ - the owner's own data only."""

    country = CountryField()

    class Meta:
        model = UserProfile
        fields = ['id', 'alternate_name', 'first_name', 'last_name', 'xp',
                  'credits', 'total_earning', 'current_earning', 'user_verified',
                  'about_me', 'steamid64', 'discord', 'xbl', 'psn', 'steam',
                  'epic', 'lol', 'battlenet', 'activisionid', 'twitter_profile',
                  'twitch_channel', 'favorite_game', 'favorite_console',
                  'profile_picture', 'user_type', 'country', 'rank',
                  'num_bronze', 'num_silver', 'num_gold', 'num_wagerwin',
                  'num_wagerloss', 'tournament_wins']
        read_only_fields = ['xp', 'credits', 'total_earning', 'current_earning',
                            'user_verified', 'user_type', 'rank', 'num_bronze',
                            'num_silver', 'num_gold', 'num_wagerwin',
                            'num_wagerloss', 'tournament_wins']


class OwnProfileUpdateSerializer(serializers.ModelSerializer):
    """Limited PATCHable fields for /api/me/."""

    country = CountryField(required=False, allow_blank=True)

    class Meta:
        model = UserProfile
        fields = ['alternate_name', 'about_me', 'steamid64', 'discord', 'xbl',
                  'psn', 'steam', 'epic', 'lol', 'battlenet', 'activisionid',
                  'twitter_profile', 'twitch_channel', 'favorite_game',
                  'favorite_console', 'country']


class MeSerializer(serializers.ModelSerializer):
    profile = OwnProfileSerializer(source='user', read_only=True)
    founder_teams = TeamSummarySerializer(many=True, read_only=True,
                                          source='user.founder_teams')
    captain_teams = TeamSummarySerializer(many=True, read_only=True,
                                          source='user.captain_teams')
    player_teams = TeamSummarySerializer(many=True, read_only=True,
                                         source='user.player_teams')
    notifications = NotificationSerializer(many=True, read_only=True,
                                           source='user.notifications')

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'date_joined', 'profile',
                  'founder_teams', 'captain_teams', 'player_teams',
                  'notifications']


class WagerRequestSerializer(serializers.ModelSerializer):
    team = TeamPrimaryKeyNestedField(queryset=Team.objects.all())
    game = serializers.PrimaryKeyRelatedField(queryset=GameChoice.objects.all())
    platform = serializers.PrimaryKeyRelatedField(queryset=PlatformChoice.objects.all())

    class Meta:
        model = WagerRequest
        fields = ['id', 'posted', 'team', 'challenge_accepted', 'expiration',
                  'expired', 'credits', 'game', 'platform', 'bestof',
                  'teamformat', 'info', 'creator']
        read_only_fields = ['posted', 'challenge_accepted', 'expired', 'creator']

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)