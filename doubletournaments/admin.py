from django.contrib import admin, messages

from .models import DoubleEliminationRound, DoubleEliminationTeam, DoubleEliminationTournament


class DoubleEliminationTeamInline(admin.TabularInline):
    model = DoubleEliminationTeam
    extra = 0
    readonly_fields = ('seed', 'eliminated', 'eliminated_round', 'placement')


@admin.register(DoubleEliminationTournament)
class DoubleEliminationTournamentAdmin(admin.ModelAdmin):
    list_display = ('name', 'active', 'size', 'teamformat', 'bestof', 'bracket_generated',
                    'current_round_winners', 'current_round_losers', 'winner')
    list_filter = ('active', 'bracket_generated', 'xp_seed', 'size', 'teamformat', 'bestof')
    search_fields = ('name',)
    filter_horizontal = ('teams',)
    inlines = (DoubleEliminationTeamInline,)
    actions = ('generate_bracket', 'advance_winners_round', 'advance_losers_round', 'reset_bracket')

    @admin.action(description='Generate bracket')
    def generate_bracket(self, request, queryset):
        for tournament in queryset:
            self.message_user(request, '%s: %s' % (tournament.name, tournament.generate_bracket()),
                              level=messages.INFO)

    @admin.action(description='Advance winners round')
    def advance_winners_round(self, request, queryset):
        for tournament in queryset:
            self.message_user(request, '%s: %s' % (tournament.name, tournament.advance_round(winners=True)),
                              level=messages.INFO)

    @admin.action(description='Advance losers round')
    def advance_losers_round(self, request, queryset):
        for tournament in queryset:
            self.message_user(request, '%s: %s' % (tournament.name, tournament.advance_round(winners=False)),
                              level=messages.INFO)

    @admin.action(description='Reset bracket')
    def reset_bracket(self, request, queryset):
        for tournament in queryset:
            self.message_user(request, '%s: %s' % (tournament.name, tournament.reset_bracket()),
                              level=messages.INFO)


@admin.register(DoubleEliminationRound)
class DoubleEliminationRoundAdmin(admin.ModelAdmin):
    list_display = ('tournament', 'bracket', 'roundnum', 'num_matches')
    list_filter = ('tournament', 'bracket')
    filter_horizontal = ('matches',)

    def num_matches(self, obj):
        return obj.matches.count()

    num_matches.short_description = 'Matches'


@admin.register(DoubleEliminationTeam)
class DoubleEliminationTeamAdmin(admin.ModelAdmin):
    list_display = ('team', 'tournament', 'seed', 'eliminated', 'eliminated_round', 'placement')
    list_filter = ('tournament', 'eliminated')