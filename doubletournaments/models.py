import math
import random

from django.db import models

from matches.models import Match, GameChoice, PlatformChoice, MapPoolChoice, SportChoice
from matches.settings import TEAMFORMAT_CHOICES, MAPFORMAT_CHOICES
from singletournaments.models import SingleTournamentRuleset
from teams.models import Team

SIZE_CHOICES = (
    (4, 4),
    (8, 8),
    (16, 16),
    (32, 32),
    (64, 64),
    (128, 128),
)

BRACKET_CHOICES = (
    ('winners', 'Winners'),
    ('losers', 'Losers'),
)

MATCH_TYPE = 'doubletournament'


class DoubleEliminationTournament(models.Model):
    name = models.CharField(max_length=50, blank=False, default='No name provided', unique=True)
    # team format, ex 1v1, 2v2, 3v3, 4v4, 5v5, 6v6
    teamformat = models.SmallIntegerField(choices=TEAMFORMAT_CHOICES, default=1)
    # finals may be best of 3, etc. in the future
    bestof = models.SmallIntegerField(choices=MAPFORMAT_CHOICES, default=1)

    # by default the tournament is not active. an admin has to activate it in order for it to be public
    active = models.BooleanField(default=False)

    # custom olly - twitch tournament
    twitch = models.CharField(max_length=60, default='twitch')

    # when does registration open, and when does it close? specified when created in staff panel
    open_register = models.DateTimeField()
    # dont allow people to join once registration is closed
    close_register = models.DateTimeField()

    # temp fix for registration since timezones are being a bitch
    allow_register = models.BooleanField(default=False)

    # general information about the tournament
    info = models.TextField(default="No information provided")

    ruleset = models.ForeignKey(SingleTournamentRuleset, related_name='doubletournamentruleset',
                                on_delete=models.PROTECT, null=True)

    # the time the specific tournament object was created
    created = models.DateTimeField(auto_now_add=True)
    # last time an admin updated something
    updated = models.DateTimeField(auto_now=True)

    req_credits = models.PositiveSmallIntegerField(default=0)

    # game and platform it will be played on
    platform = models.ForeignKey(PlatformChoice, on_delete=models.PROTECT, null=True, blank=True)
    game = models.ForeignKey(GameChoice, related_name='de_game', on_delete=models.PROTECT, null=True, blank=True)

    sport = models.ForeignKey(SportChoice, related_name='de_sport', on_delete=models.PROTECT, null=True, blank=True)

    # when will the first round of matches start?
    start = models.DateTimeField()

    # all the teams that are in the event. eligibility happens inside the view
    teams = models.ManyToManyField(Team, blank=True)

    # specify the winning team when they are declared
    winner = models.ForeignKey(Team, related_name='de_winningteam', on_delete=models.SET_NULL, blank=True, null=True)

    # specify second place, just for storage and future reference
    second = models.ForeignKey(Team, related_name='de_secondplaceteam', on_delete=models.SET_NULL, blank=True,
                               null=True)

    third = models.ForeignKey(Team, related_name='de_thirdplaceteam', on_delete=models.SET_NULL, blank=True, null=True)

    # specify how many teams the event will be capped at, and the size of the bracket
    size = models.PositiveSmallIntegerField(default=32, choices=SIZE_CHOICES)

    xp_seed = models.BooleanField(default=False)

    bracket_generated = models.BooleanField(default=False)

    map_pool = models.ForeignKey(MapPoolChoice, related_name='de_map_pool', on_delete=models.SET_NULL, null=True)

    # the prizes that they will win, defined in admin panel
    prize1 = models.CharField(default='no prize specified', max_length=50)
    prize2 = models.CharField(default='no prize specified', max_length=50)
    prize3 = models.CharField(default='no prize specified', max_length=50)

    image = models.ImageField(upload_to='tournament_images', blank=True)

    # if set to true, admins will have manually input the result of each match, users will not be able to report wins
    disable_userreport = models.BooleanField(default=True)

    # track round progress in each bracket
    current_round_winners = models.PositiveSmallIntegerField(default=1)
    current_round_losers = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return self.name

    # ------------------------------------------------------------------
    # bracket helpers
    # ------------------------------------------------------------------

    @property
    def winners_rounds(self):
        return self.de_rounds.filter(bracket='winners').order_by('roundnum')

    @property
    def losers_rounds(self):
        return self.de_rounds.filter(bracket='losers').order_by('roundnum')

    @property
    def winners_round_count(self):
        # number of winners-bracket rounds before the grand final
        return int(math.log2(self.size))

    @property
    def losers_round_count(self):
        # number of losers-bracket rounds (a double-elimination bracket with
        # W winners rounds has 2W-2 losers rounds)
        return 2 * self.winners_round_count - 2

    def _get_round(self, bracket, roundnum):
        try:
            return self.de_rounds.get(bracket=bracket, roundnum=roundnum)
        except DoubleEliminationRound.DoesNotExist:
            return None

    def _get_or_create_round(self, bracket, roundnum):
        round_obj = self._get_round(bracket, roundnum)
        if round_obj is None:
            round_obj = DoubleEliminationRound.objects.create(tournament=self, bracket=bracket, roundnum=roundnum)
        return round_obj

    def _xp_key(self, team):
        # seed by the founder's UserProfile xp, highest xp first
        if team.founder is None:
            return 0
        try:
            return team.founder.user.xp
        except AttributeError:
            return 0

    def _seed_teams(self):
        teams = list(self.teams.all())
        if self.xp_seed:
            teams.sort(key=self._xp_key, reverse=True)
        else:
            random.shuffle(teams)
        return teams

    def _make_match(self, awayteam, hometeam):
        return Match(
            type=MATCH_TYPE,
            awayteam=awayteam,
            hometeam=hometeam,
            game=self.game,
            platform=self.platform,
            sport=self.sport,
            map_pool=self.map_pool,
            bestof=self.bestof,
            teamformat=self.teamformat,
            disable_userreport=self.disable_userreport,
        )

    def _make_bye_match(self, team):
        match = self._make_match(awayteam=team, hometeam=None)
        match.bye_1 = True
        match.winner = team
        match.completed = True
        return match

    def _round_matches_ready(self, round_obj):
        if round_obj is None or round_obj.matches.count() == 0:
            return False
        for match in round_obj.matches.all():
            if not match.completed or match.winner is None:
                return False
        return True

    def _all_matches_ready(self, round_obj):
        # an empty round counts as trivially complete
        if round_obj is None:
            return False
        for match in round_obj.matches.all():
            if not match.completed or match.winner is None:
                return False
        return True

    def _winners_champion(self):
        wround = self._get_round('winners', self.winners_round_count)
        if wround is None or wround.matches.count() != 1:
            return None
        return wround.matches.first().winner

    def _losers_champion(self):
        lround = self._get_round('losers', self.losers_round_count)
        if lround is None or lround.matches.count() == 0:
            return None
        return lround.matches.first().winner

    def _set_eliminated(self, team, roundnum):
        entry, _ = DoubleEliminationTeam.objects.update_or_create(
            tournament=self, team=team,
            defaults={'eliminated': True, 'eliminated_round': roundnum})
        # placement is 1-based: number of teams still alive after this
        # elimination, plus one
        entry.placement = DoubleEliminationTeam.objects.filter(
            tournament=self, eliminated=False).count() + 1
        entry.save()
        return entry

    def _set_placement(self, team, placement):
        DoubleEliminationTeam.objects.filter(tournament=self, team=team).update(placement=placement)

    def _get_third_place(self):
        lround = self._get_round('losers', self.losers_round_count)
        if lround is None or lround.matches.count() == 0:
            return None
        return lround.matches.first().loser

    def _complete_tournament(self, match):
        winner_team = match.winner
        loser_team = match.loser
        if loser_team is None:
            loser_team = match.hometeam if match.hometeam and match.hometeam.pk != winner_team.pk else match.awayteam
        self._set_eliminated(loser_team, self.winners_round_count + 1)
        self._set_placement(winner_team, 1)
        self.winner = winner_team
        self.second = loser_team
        self.third = self._get_third_place()
        self.save()

    # ------------------------------------------------------------------
    # bracket generation
    # ------------------------------------------------------------------

    def generate_bracket(self):
        if self.bracket_generated:
            return 'Bracket already generated'
        count = self.teams.count()
        if count < 2:
            return 'Not enough teams registered (need at least 2)'
        if count > self.size:
            return 'Too many teams registered for bracket size'
        teams = self._seed_teams()
        DoubleEliminationTeam.objects.filter(tournament=self).delete()
        for index, team in enumerate(teams, start=1):
            DoubleEliminationTeam.objects.create(tournament=self, team=team, seed=index)
        # create all rounds as empty shells; matches for later rounds are
        # created when a round is advanced
        for roundnum in range(1, self.winners_round_count + 1):
            DoubleEliminationRound.objects.create(tournament=self, bracket='winners', roundnum=roundnum)
        for roundnum in range(1, self.losers_round_count + 1):
            DoubleEliminationRound.objects.create(tournament=self, bracket='losers', roundnum=roundnum)
        # winners round 1: the highest seeds receive byes, the remaining
        # lowest seeds play adjacent pairs (the standard bracket order for
        # seeded tournaments: [0]vs[1], [2]vs[3], ...)
        byes = self.size - count
        round1 = self._get_round('winners', 1)
        playing = teams[byes:]
        for i in range(0, len(playing), 2):
            match = self._make_match(awayteam=playing[i], hometeam=playing[i + 1])
            match.save()
            round1.matches.add(match)
        for team in teams[:byes]:
            match = self._make_bye_match(team)
            match.save()
            round1.matches.add(match)
        self.bracket_generated = True
        self.current_round_winners = 1
        self.current_round_losers = 1
        self.save()
        return 'Bracket generated for %s teams' % count

    # ------------------------------------------------------------------
    # round advancement
    # ------------------------------------------------------------------

    def advance_round(self, winners=True):
        if winners:
            return self._advance_winners()
        return self._advance_losers()

    def _advance_winners(self):
        if not self.bracket_generated:
            return 'Bracket has not been generated yet'
        w = self.current_round_winners
        if w > self.winners_round_count + 2:
            return 'Tournament already complete'
        wround = self._get_round('winners', w)
        if wround is None:
            return 'No winners round %s' % w
        if w > self.winners_round_count:
            return self._advance_grand_final(w, wround)
        if not self._round_matches_ready(wround):
            return 'Winners round %s is not complete yet' % w
        if w < self.winners_round_count:
            next_round = self._get_round('winners', w + 1)
            if next_round is not None and next_round.matches.count() > 0:
                return 'Winners round %s has already been advanced' % w
        else:
            gf_round = self._get_round('winners', w + 1)
            if gf_round is not None and gf_round.matches.count() > 0:
                return 'Winners round %s has already been advanced' % w
        # pair the winners in match order into the next winners round
        winners = [match.winner for match in wround.matches.all().order_by('id')]
        # feed the losers of this winners round into the matching losers round
        self._create_losers_round(w)
        if w < self.winners_round_count:
            next_round = self._get_or_create_round('winners', w + 1)
            for i in range(0, len(winners), 2):
                match = self._make_match(awayteam=winners[i], hometeam=winners[i + 1])
                match.save()
                next_round.matches.add(match)
            self.current_round_winners = w + 1
            self.save()
            return 'Advanced winners round %s' % w
        # last winners round: the survivor is the winners-bracket champion
        self.current_round_winners = w + 1
        self.save()
        if self._create_grand_final():
            return 'Winners champion decided; grand final created'
        return 'Winners champion decided; waiting for losers bracket'

    def _advance_grand_final(self, w, wround):
        if wround.matches.count() == 0:
            return 'Waiting for the losers bracket to finish'
        if not self._round_matches_ready(wround):
            return 'Grand final round is not complete yet'
        match = wround.matches.first()
        winners_champion = self._winners_champion()
        if match.winner is None or winners_champion is None:
            return 'Grand final round is not complete yet'
        if w == self.winners_round_count + 1 and match.winner.pk != winners_champion.pk:
            # the losers-bracket champion won the first grand final: bracket
            # reset, play a second grand final
            reset_round = self._get_or_create_round('winners', w + 1)
            if reset_round.matches.count() > 0:
                return 'Grand final has already been advanced'
            reset_match = self._make_match(awayteam=match.awayteam, hometeam=match.hometeam)
            reset_match.save()
            reset_round.matches.add(reset_match)
            self.current_round_winners = w + 1
            self.save()
            return 'Bracket reset: second grand final created'
        self._complete_tournament(match)
        return 'Tournament complete: %s is the champion' % match.winner.name

    def _advance_losers(self):
        if not self.bracket_generated:
            return 'Bracket has not been generated yet'
        k = self.current_round_losers
        if k > self.losers_round_count:
            return 'Losers bracket is complete'
        lround = self._get_round('losers', k)
        if lround is None:
            return 'No losers round %s' % k
        if lround.matches.count() == 0:
            # nothing was fed into this round (all byes); skip it
            self._create_losers_round(k + 1)
            self.current_round_losers = k + 1
            self.save()
            return 'Losers round %s had no matches; skipped' % k
        if not self._round_matches_ready(lround):
            return 'Losers round %s is not complete yet' % k
        if k == self.losers_round_count:
            # last losers round: winner is the losers-bracket champion, loser
            # takes third place
            for match in lround.matches.all().order_by('id'):
                if match.loser is not None:
                    self._set_eliminated(match.loser, k)
            self.current_round_losers = k + 1
            self.save()
            if self._create_grand_final():
                return 'Losers champion decided; grand final created'
            return 'Losers champion decided; waiting for winners bracket'
        # eliminate the losers of this losers round
        for match in lround.matches.all().order_by('id'):
            if match.loser is not None:
                self._set_eliminated(match.loser, k)
        self._create_losers_round(k + 1)
        self.current_round_losers = k + 1
        self.save()
        return 'Advanced losers round %s' % k

    def _create_losers_round(self, k):
        if k < 1 or k > self.losers_round_count:
            return None
        lround = self._get_round('losers', k)
        if lround is None or lround.matches.count() > 0:
            return None
        if k == 1:
            # losers round 1: losers of winners round 1, paired in match order
            w1 = self._get_round('winners', 1)
            if not self._round_matches_ready(w1):
                return None
            participants = [match.loser for match in w1.matches.all().order_by('id') if match.loser is not None]
        else:
            # losers round k (k >= 2): winners of losers round k-1 face the
            # losers of winners round k, interleaved in match order
            prev = self._get_round('losers', k - 1)
            if not self._all_matches_ready(prev):
                return None
            wk = self._get_round('winners', k) if k <= self.winners_round_count else None
            if wk is not None and not self._round_matches_ready(wk):
                return None
            winners_prev = [match.winner for match in prev.matches.all().order_by('id')]
            losers_curr = [match.loser for match in wk.matches.all().order_by('id')] if wk else []
            participants = []
            for i in range(max(len(winners_prev), len(losers_curr))):
                if i < len(winners_prev):
                    participants.append(winners_prev[i])
                if i < len(losers_curr):
                    participants.append(losers_curr[i])
        if not participants:
            return None
        for i in range(0, len(participants), 2):
            if i + 1 < len(participants):
                match = self._make_match(awayteam=participants[i], hometeam=participants[i + 1])
            else:
                match = self._make_bye_match(participants[i])
            match.save()
            lround.matches.add(match)
        return lround

    def _create_grand_final(self):
        gf_round = self._get_or_create_round('winners', self.winners_round_count + 1)
        if gf_round.matches.count() > 0:
            return False
        winners_champion = self._winners_champion()
        losers_champion = self._losers_champion()
        if winners_champion is None or losers_champion is None:
            return False
        match = self._make_match(awayteam=winners_champion, hometeam=losers_champion)
        match.save()
        gf_round.matches.add(match)
        return True

    # ------------------------------------------------------------------
    # admin helpers
    # ------------------------------------------------------------------

    def reset_bracket(self):
        matches = []
        for round_obj in self.de_rounds.all():
            matches.extend(round_obj.matches.all())
        for round_obj in self.de_rounds.all():
            round_obj.matches.clear()
        self.de_rounds.all().delete()
        for match in matches:
            match.delete()
        DoubleEliminationTeam.objects.filter(tournament=self).update(
            eliminated=False, eliminated_round=0, placement=0)
        self.bracket_generated = False
        self.current_round_winners = 1
        self.current_round_losers = 1
        self.winner = None
        self.second = None
        self.third = None
        self.save()
        return 'Bracket reset'


class DoubleEliminationRound(models.Model):
    tournament = models.ForeignKey(DoubleEliminationTournament, related_name='de_rounds',
                                   on_delete=models.CASCADE)
    bracket = models.CharField(max_length=10, choices=BRACKET_CHOICES, default='winners')
    roundnum = models.PositiveSmallIntegerField(default=1)
    matches = models.ManyToManyField(Match, blank=True)

    def __str__(self):
        return '%s %s round %s' % (self.tournament.name, self.get_bracket_display(), self.roundnum)


class DoubleEliminationTeam(models.Model):
    team = models.ForeignKey(Team, related_name='de_team_entries', on_delete=models.CASCADE)
    tournament = models.ForeignKey(DoubleEliminationTournament, related_name='de_teams_entries',
                                   on_delete=models.CASCADE)
    seed = models.PositiveIntegerField(default=0)
    eliminated = models.BooleanField(default=False)
    eliminated_round = models.PositiveSmallIntegerField(default=0)
    placement = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return '%s in %s (seed %s)' % (self.team.name, self.tournament.name, self.seed)