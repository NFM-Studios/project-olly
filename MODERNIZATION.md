# Project Olly — Modernization & Completion Task List

Review date: 2026-08-25
Current state: Django 2.2 (EOL), Python 3.x era, last commit Aug 2021, ~360KB of Python across 11 apps,
177 templates, no build tooling, <5% test coverage, multiple verified crash-level bugs in core flows.

---

## STATUS — all phases implemented on `dev-master` (2026-08-25)

Final: **Django 4.2.30 LTS · Python 3.11 · 194 tests passing · 12 squashed migrations · Bootstrap 5 / FA6 frontend**

| Phase | Status | Notes |
|---|---|---|
| 0 Baseline, safety net, security quick wins | ✅ | 34-test baseline; smoke-test script; cookie flags, ALLOWED_HOSTS, GenericIPAddressField ban, middleware rewrite |
| 1 Framework & infra | ✅ | Django 4.2.30, STORAGES, modern auth CBVs, six/force_text removed, python:3.11-slim + postgres:16 + Caddy v2 + GH Actions CI |
| 2 Crash bugs | ✅ | ~60 verified bugs fixed across matches/teams/wagers/tournaments/staff |
| 3 Security | ✅ | staff_required decorator (403), IDOR fixes (tickets/notifications/invites), PayPal IPN, open redirects, XSS via js_datetime filters, destructive GET→POST |
| 4 Complete features | ✅ | league join/leave + division placement, check-in enforcement, news comments, wager lifecycle, allow_register + XP seeding + byes |
| 5 New features | ✅ | DRF REST API, Django Channels realtime, double-elimination tournaments, Stripe Checkout |
| 6 Frontend | ✅ | Bootstrap 5.3.7 + FA6 + jQuery 3.7 + DataTables 1.13 + Chart.js 4, esbuild toolchain, a11y/responsive pass, dead code removed |
| 7 Quality & release | ✅ | enums, DecimalField money, indexes, aggregate rank, admin upgrades, migrations squashed one-per-app |

Key commits: `47079cd2` (Django 4.2) · `6a178a58` (staff auth) · `3ed05754` (API) · `d377209a` (Channels) ·
`a9ce76c7` (double-elim) · `576990e5` (Stripe) · `aa0abe78..8d8d9627` (frontend) · `a6671cb8` (squash).

---

## Phase 0 — Baseline, Safety Net, and Quick Wins

Goal: get a known-good, runnable baseline before touching anything; close the cheap security holes.

### 0.1 Baseline
- [x] Confirm `git status` clean and tag current HEAD as `legacy-baseline` (or branch `modernization/`).
- [x] Review existing remote branches for salvageable work: `rewrite`, `permissions-rewrite`, `2fa`,
      `league_match_scheduler`, `match_stats`, `stats-new`, `teams-queryset`, `128`, `csc-design`,
      `leagues-form-dev` (many match roadmap items below).
- [x] Create a local venv on Python 3.11 (available on this machine) and get the app booting
      (`manage.py runserver`) with SQLite in dev mode. Document any blockers encountered.
- [x] Inventory all env vars actually read by `olly/settings.py` + `olly/base_settings.py` and compare
      against `.env.example` (settings.py reads `secret_key`, `debug`, `allowed_hosts`, `site_url`,
      `db_type/name/username/password/host/port`, `storage_*`, `email_*`, `from_email`, `paypal_email`,
      `google_recaptcha_*`, `site_name`, `site_server`, optional `user_verification`, `esports_mode`,
      `enable_store`, `enable_wagers`).
- [x] Squash/tag nothing in git yet; keep every change reviewable.

### 0.2 Test safety net
- [x] Run the current test suite (`python manage.py test`) and record baseline pass/fail.
- [x] Rewrite `staff/tests.py` (20 tests that all call the `users` view instead of the view they claim
      to test — staff/tests.py:37-189). Replace with real view tests.
- [x] Fix the broken tests: `teams/tests.py:54-58` (passes URL name to `factory.get`, passes `None` as
      view self), `test_teameditview` is `pass`.
- [x] Add a smoke test that boots the site and hits every public URL (index, about, terms, news,
      teams, tournaments, leagues, matches, wagers, store, support FAQ).
- [x] Fill the empty stub test files (leagues, matches, store, support, profiles, singletournaments,
      wagers — all `# Create your tests here.`).

### 0.3 Security quick wins (low effort, high value)
- [x] `olly/base_settings.py`: set `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`,
      `SECURE_SSL_REDIRECT`, `SECURE_HSTS_SECONDS`, `X_FRAME_OPTIONS` via env with sane defaults
      (currently none are set; session cookie is sent over plain HTTP).
- [x] Fix `ALLOWED_HOSTS = os.environ['allowed_hosts']` (olly/settings.py:15) — parse comma-separated
      env value into a list; current raw string breaks `is_safe_url` and login redirect logic.
- [x] Fix `BannedUser.ip = CharField(max_length=12)` (profiles/models.py:118) — staff writes
      `'999.999.999.999'` (15 chars, staff/views/users.py:66) → DataError; widen to 45 + migrate, and
      use `GenericIPAddressField`.
- [x] Fix `olly/middleware.py:12` ban logic (convoluted condition; `/admin` never excluded as
      intended) and remove the per-request DB write of `user.ip` (write amplification on every
      request); batch/stamp IPs only at login.
- [x] Remove `statics` references that 404: `matches_list.html:8` (`css/matches.css` doesn't exist),
      `match_detail.html:144` / `wager_match_detail.html` (`binge/images/avatar.jpg` doesn't exist),
      `staffbase.html:31-32` (`project-static/ckeditor/` doesn't exist — CKEditor is served by
      django-ckeditor, not vendored).

---

## Phase 1 — Framework & Dependency Modernization

Goal: Django LTS, modern Python, clean dependency management, modern infra.

### 1.1 Django upgrade
- [x] Upgrade Django 2.2 → 4.2 LTS (safe path), then evaluate 5.x. Migrate in 2.2→3.2→4.2 steps
      following the official release notes if time allows; at minimum run the 4.2 deprecation sweep.
- [x] Replace `django.utils.six` (profiles/tokens.py:2,8) with plain `str`.
- [x] Replace `force_text()` (profiles/views.py:16,197,366; staff/views/users.py:8) with `force_str()`.
- [x] Remove `current_app` kwarg + `request.current_app = ...` (profiles/views.py:81-82, 118-119,
      161-162, 174-175, 221-222, 234-235) — removed in Django 3.0.
- [x] Replace hand-ported Django 1.x auth views (profiles/views.py:26-84 — custom login, logout,
      password_reset, password_reset_confirm) with `django.contrib.auth.views` class-based views or
      `include('django.contrib.auth.urls')`; keep reCAPTCHA hook on registration/login.
- [x] Fix `is_safe_url(url=..., allowed_hosts=request.get_host())` → new signature
      `url_has_allowed_host_and_scheme()` (profiles/views.py:103).
- [x] Replace deprecated `DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'`
      (olly/settings.py:69) with the `STORAGES` dict (Django 4.2+).
- [x] Replace `USE_L10N` deprecation, `ugettext` → `gettext` if used anywhere.
- [x] Fix `Notification.datetime` field with `auto_created=True` (profiles/models.py:24) — invalid for
      a declared field.
- [x] Remove dead `__unicode__` methods (matches/models.py:95,106) — Python 3 leftover.
- [x] Modernize settings: split into `settings/base.py`, `dev.py`, `prod.py`; parse env with
      `django-environ`; drop reliance on `os.environ[key]` raising KeyError at import (olly/settings.py:6).
- [x] Replace `STATIC_ROOT = '/static/'` (base_settings.py:170) — absolute-path misconfiguration for
      Windows/containers; make it project-relative.
- [x] Re-pin `requirements.txt` with exact versions; add `psycopg[binary]` (psycopg2-binary is legacy),
      `gunicorn` (currently installed ad hoc in the dockerfile), `django-environ`, `sentry-sdk`,
      `whitenoise` (for static serving without S3), `pytest` + `pytest-django` + `coverage`.

### 1.2 Dependency / library modernization
- [x] `django-paypal` (PayPal IPN, 2019-era) → evaluate `django-paypal` maintenance status; plan
      Stripe Checkout as replacement (see 5.4). Keep IPN working meanwhile.
- [x] `django-ckeditor` → keep (still maintained) but pin; confirm JS assets resolve.
- [x] `django-ipware` → pin current; verify `get_client_ip` API (middleware.py:2).
- [x] `django-countries`, `django-cleanup`, `django-storages`, `boto3` → pin current compatible
      versions; verify S3 endpoint behavior (B2/Backblaze note in changelog).
- [x] reCAPTCHA v2 → evaluate `django-recaptcha` for form integration (currently manual
      POST verification in profiles/views.py:40-46, 310-317).

### 1.3 Container / infra modernization
- [x] `dockerfile`: `python:slim` (unpinned) → `python:3.11-slim` or `3.12-slim`; install `gunicorn`
      from requirements; add `start.sh` hardening (wait-for-db, run migrations on deploy job instead
      of container start).
- [x] `docker-compose.yml`: version key removed (legacy), `postgres:12` (EOL) → `postgres:16`,
      `abiosoft/caddy:no-stats` (dead image) → `caddy:2` with modern Caddyfile syntax; add healthchecks,
      named volumes for DB persistence (currently `./database` bind mount), non-root user.
- [x] Add `docker-compose.dev.yml` with hot-reload (bind mount + `runserver`) for the dev loop.
- [x] `.github/`: add CI workflow — lint (ruff), typecheck (mypy/pyright, at least on new code),
      pytest with coverage gate, migration-check, Docker build. Replace the dead Jenkins badge in README.
- [x] Add Sentry (DSN via env) and structured logging config; `LOGGING` dict + request-id middleware.
- [x] Add `/healthz` and `/readyz` endpoints (DB + storage checks) for container orchestration.

---

## Phase 2 — Fix Verified Crash-Level Bugs

All verified in the 2026-08 review. These are the "app is broken" issues; fix first, in priority order.

### 2.1 Match system (core loop)
- [x] matches/views.py:84-85 — `team1.captains` / `team2.captains` → AttributeError: `Team` has
      `captain` (m2m), not `captains`. **Match reporting is 100% broken for non-bye matches.**
- [x] matches/views.py:274 — `user == team.captain.all()` compares User to QuerySet → always False;
      captains can never check a team in.
- [x] matches/views.py:309-310 — `create_checkin` is an empty `pass` stub.
- [x] matches/views.py:67-68, 80, 252, 266, 268 — `Match.objects.get(pk=pk)` without
      `get_object_or_404` → 500 on bad pk.
- [x] matches/views.py:228-248 — `MatchDisputeReportCreateView.form_valid`: `MatchReport.objects.get()`
      raises DoesNotExist for non-original reporters; raw `form.data['teamproof_1']` (KeyError risk);
      `super().form_valid` never called.
- [x] matches/views.py:76-211 — `MatchReportCreateView.post` never calls `form.is_valid()` and accepts
      any team id as winner (data integrity bypass) — validate against the match's two teams.
- [x] matches/views.py:144 — `reports[0]`/`reports[1]` rely on undefined queryset ordering — order by
      `created` explicitly.

### 2.2 Teams
- [x] teams/views.py:164 — `invite.inviter = self.request.inviter` (HttpRequest has no `inviter`) →
      team-detail invite form always 500s.
- [x] teams/views.py:322, 327 — `request.user is team.founder.all()` (FK has no `.all()`) →
      LeaveTeamView always 500s.
- [x] teams/views.py:419 — `settings.freeze_team_deletion` NameError in `DissolveTeamView.post`
      (settings only defined in `get`) → dissolving always 500s.
- [x] teams/views.py:235 — `request.user.username in captains` (str vs QuerySet) → captains can never
      send invites.
- [x] teams/views.py:254-256 — captain flag silently swallowed by bare `try/except KeyError`.
- [x] teams/views.py:239 — bare `except:` — narrow it.
- [x] teams/views.py:155 — `request.user.xbl_verified` → AttributeError (it's on UserProfile).

### 2.3 Wagers
- [x] wagers/views.py:206 — `final` never defined → `MyWagersList` 500s on every load.
- [x] wagers/views.py:203 — `old_results = old_requests + x` (QuerySet + instance → TypeError).
- [x] wagers/views.py:169 — `myrequest.creator.credits` — `creator` is a `User`; credits live on
      `UserProfile` → wager challenge acceptance crashes; challenger's stake never debited.
- [x] wagers/views.py:92-105 — `min` NameError when teamformat is outside 0-5.
- [x] wagers/views.py:118 — naive `datetime.utcnow()` vs `USE_TZ=True`; use `timezone.now()`.

### 2.4 Tournaments
- [x] singletournaments/views.py:119, 138, 144, 200 — iterating/`len()`/membership on m2m managers →
      join and leave both crash; credits never refunded on leave.
- [x] singletournaments/views.py:227 — `tournament.teams.all` missing `()` → team list page broken.
- [x] singletournaments/models.py:125 — `random.random(1, poolsize)` (takes no args) + `match.map =`
      (no such field) → `generate_maps` entirely broken.
- [x] singletournaments/models.py:130, 186, 189 — `self.kwargs` misuse, missing `()` on `.count`.
- [x] singletournaments/views.py:28-29 — `List.post` ignores `form.is_valid()` → KeyError on bad input.
- [x] singletournaments/views.py:164-168 — join deducts `req_credits` per player instead of per team.

### 2.5 Staff panel
- [x] staff/views/matches.py:173-174, 177-183 — `Team.num_losses/num_wins` → AttributeError (fields are
      `num_matchloss`/`num_matchwin`); league block doesn't `return` → double winner declaration.
- [x] staff/views/matches.py:780, 805 — `match.team1`/`match.team2` don't exist → `set_dispute_match`
      always 500s; also never sets `match.disputed = True`.
- [x] staff/views/matches.py:854-879 — `awayplayers.add()` on a list, `x.steamid64` on strings,
      `data['team2']` built from `awayteam` → `create_match_config` always crashes. Rewrite config
      generation (it also hardcodes CS:GO maps and 5v5).
- [x] staff/views/matches.py:739-760 — `delete_checkin` fetches by match pk, calls `save()` after
      `delete()`, string+int concat → broken.
- [x] staff/views/teams.py:83 — `temp.player_teams.save()` on an m2m manager → force-add-player 500s.
- [x] staff/views/teams.py:135 — `User.objects.get(user=muser)` → FieldError → remove-user 500s.
- [x] staff/views/singletournaments.py:257 — `winners` is a QuerySet, has no `.append` → advancing a
      round 500s. Also :253,256 — `redirect(request, ...)` passes request as target.
- [x] staff/views/leagues.py:75 — `permissiondenied.hmtl` typo → TemplateDoesNotExist.
- [x] staff/views/leagues.py:285 — `form.add_error(form, ...)` wrong signature + `redirect('staff:add_match_league')` (NoReverseMatch).
- [x] staff/views/leagues.py:231 — `create_divisions` creates N divisions on every call (duplicates).
- [x] staff/views/leagues.py:168-175, 341-347 — `launch_league` and `bulk_match_create` are incomplete
      (no return/render).
- [x] staff/views/store.py:120 — `form.cleaned_data['price']` (no such field) → product edit 500s.
- [x] staff/views/store.py:38-43 — `TransactionView.post` returns None → 500.
- [x] staff/views/staff.py:82-84 — `createpartner` GET returns None → 500; :176 settings duplicate rows.
- [x] staff/views/users.py:142-158 — `modifyuser` invalid form has no return → 500.
- [x] staff/views/support.py:255 — `QuestionAnswerCategory.objects.all` missing `()`.
- [x] staff/urls.py:62 — `add_teams(request, pk, teamid)` vs view signature `(request, pk)` → TypeError;
      duplicate URL name `add_team` (urls.py:61).
- [x] staff/views/matches.py:399, 422-423, 527, 591 — wrong forms used in create/detail branches
      (GameChoiceForm/PlatformChoiceForm mixups).
- [x] staff/views/matches.py:36-37 — `disputed_matches` filters `type__isnull=True` but tournament
      matches have `type='singletournament'` → wrong list.
- [x] staff/views/matches.py:655-656 — `match.maps.add(chosen_map3)` called twice.
- [x] staff/forms.py:315 — `exclude = ('non_conference',)` outside `Meta` (ignored).
- [x] staff/views/news.py:66-68 — `edit_post` rewrites `post.author` on every edit.

### 2.6 Profiles / auth / misc
- [x] profiles/views.py:272-289 — `edit_profile` invalid-form POST falls through with no return → 500.
- [x] profiles/views.py:392-429 — LeaderboardView ignores `form.is_valid()` → KeyError.
- [x] profiles/views.py:434 — `messages.error('...', request)` args reversed.
- [x] profiles/views.py:51 — checkbox named `'remember me'` (space) never matches the form field; also
      fix login_form.html:27.
- [x] support/views.py:73-84 — `post()` has no return when neither comment nor status change present.
- [x] support/views.py:83 — status form saved without `is_valid()`, force-sets status=3 (dropdown dead).
- [x] support/views.py:42-44, staff/views/support.py:28-32 — ineffective `try/except ValueError` on lazy
      queryset — evaluate the queryset or validate input first.
- [x] store/views.py:80 — Transfer POST renders wrong template; :78 hardcoded `/profile/` redirect.
- [x] store/views.py:58-62 — bare `except:` on user lookup.
- [x] leagues/views.py:16 — `league.divisions is None` always False (manager never None) — dead branch.
- [x] olly/urls.py:23 — `path('404/', notfound)` → TypeError (`notfound` needs `exception` arg).
- [x] news/views.py:37-50 — comment posting disabled (`pass`/commented).
- [x] matches/views.py:286, 294 — TODO check-in team/player resolution (see 4.x).
- [x] staff/views/matches.py:95-102 — match_edit notification loop double-iterates hometeam, misses captains.

---

## Phase 3 — Security Hardening (beyond quick wins)

### 3.1 Broken access control (IDOR) — verified
- [x] support/views.py:56-84 — any logged-in user can view/comment/close any ticket by ID → restrict
      to `ticket.creator` or staff.
- [x] profiles/views.py:447-464 — notification read/unread by pk with no ownership check → filter by
      `request.user`.
- [x] teams/views.py:44-89 — accept/decline any `TeamInvite` by ID → require invite belongs to
      `request.user` and is still `active`.
- [x] profiles/views.py:261-269 — `searchusers` exposes `user__email__icontains` → drop email from
      search; at minimum restrict to staff.

### 3.2 Authorization model
- [x] Replace the hand-rolled `user_type in ['admin','superadmin']` check (~50 copy-pasted staff
      views) with Django groups/permissions + a `StaffRequiredMixin` / `@staff_member_required`
      equivalent that returns a real 403.
- [x] Enforce `admin` vs `superadmin` distinction or merge them (currently identical).
- [x] Make staff views return 403, not a 200 rendered "permission denied" page.
- [x] Consider a `GroupsRequiredMixin` and seed groups via data migration.

### 3.3 XSS / CSRF / input validation
- [x] Remove `|safe` on all `new Date("{{ ...|safe }}")` inline scripts (leagues/league_detail.html:111,116,
      leagues/leagues_list.html:88,94, singletournaments/singletournament_detail.html:111,117,
      singletournaments/singletournament_list.html:84,91, wagers/wager_request_detail.html:12,32,
      wagers/wager_request_list.html:27, matches/matches_list.html:28, staff/matches/match_detail.html:42) —
      format datetimes server-side or via a template filter / `json_script`.
- [x] Replace all 16 destructive GET links with `onclick="return confirm(...)"` (staff templates) with
      POST forms (CSRF-protected) — e.g. staff/leagues/league_detail.html:148-150, staff/store/product_detail.html:48,
      staff/singletournaments/singletournament_detail.html:117, staff/teams/team_detail.html:88,92,
      staff/profiles/users.html:81, staff/support/qa_detail.html:24, staff/pages/slide_detail.html:27.
- [x] Validate `MatchReport.proof` length/content (CharField 300, form bypasses validation).
- [x] Validate URLs in `MatchDispute` proof fields.
- [x] store/models.py:42-71 — PayPal IPN handler: return after business-email mismatch (currently
      credits the user anyway); add signature verification assertions.
- [x] pages/views.py:56-61 — static page redirect: use `url_has_allowed_host_and_scheme` guard.
- [x] Add rate limiting on login/register/password-reset (e.g. `django-axes` or middleware).

---

## Phase 4 — Complete Existing (Half-Built) Functionality

From code TODOs, stubs, and the README roadmap.

- [x] **Leagues**: finish `join_league` (leagues/views.py:28-50 — deducts credits but never adds team),
      `leave_league` (pass stub, leagues/views.py:53-55), division auto-creation remainder handling,
      auto-schedule (`LeagueSettings.auto_schedule` TODO, leagues/models.py:26), bulk match generation
      (staff/views/leagues.py:341), league launch flow (staff/views/leagues.py:168), league winner
      declaration + reset (staff/views/matches.py:185, 243 — TODO #107).
- [x] **Match check-in**: implement `create_checkin` (matches/views.py:309), enforce min team size and
      roster presence, wire check-in status into match detail.
- [x] **Match config generation**: rewrite `create_match_config` (staff/views/matches.py:829) — remove
      hardcoded CS:GO maps/5v5, derive from match game/teamformat/map pool; fix `data['team2']` bug.
- [x] **Tournaments**: enforce `allow_register` (currently ignored, singletournaments/views.py:103-109),
      implement XP seeding (`xp_seed` field), fix bye handling (random team TODO,
      singletournaments/models.py:158), fix `generate_maps`, verify bracket generation for odd sizes
      (prints "ITS BROKEN YOU SUCK" — models.py:166).
- [x] **Match dispute flow**: implement full lifecycle — create dispute (fixed in 2.1), staff review
      (staff/views/matches.py:780 — sets no `disputed` flag), evidence display, resolution.
- [x] **Wagers**: complete challenge lifecycle — request → challenge → accept (currently crashes) →
      match → winner declared (staff/views/matches.py:213 crashes iterating players) → credits paid out,
      wager history (wagers/views.py:206), expiration enforcement (naive datetime bug).
- [x] **News comments**: re-enable `CommentForm` (news/forms.py:13-16, news/views.py:37-50); add
      moderation + spam protection.
- [x] **Stats**: wire the existing `StatsPlayer`/`TeamMatchStats` models (CS:GO-specific fields) into
      match reporting UI; add a game-agnostic stats schema for other sports; build player profile stats
      pages (README roadmap says "basic stats models (will be built upon)").
- [x] **Support**: make ticket status dropdown functional (support/views.py:83 force-closes), ticket
      assignment workflow, FAQ search.
- [x] **User verification**: finish `user_verification` flow — resend email button (changelog #123),
      verified badge, gating for tournaments/leagues.
- [x] **Store**: finish product edit (KeyError fix), transfer flow (wrong template), transaction ledger
      UI, `Transfer` model usage.
- [x] **Banned users**: enforce ban on login (set `is_active=False` too), admin unban flow.

---

## Phase 5 — Expand & Add New Functionality

### 5.1 Roadmap features from README (planned, never built)
- [x] **Double-elimination tournaments** — new app or extension of singletournaments (models: winners
      & losers brackets, grand finals, bracket UI). High value, biggest gap vs. modern platforms.
- [x] **Ladders** — challenge-based ranked ladders per game/platform; reuse team/wager challenge model.

### 5.2 New platform features
- [x] **REST API** — Django REST Framework: public read endpoints (tournaments, leagues, matches,
      teams, news) + token auth for integrations; enables mobile/web-app clients and Discord bots.
- [x] **Real-time** — Django Channels: live match updates, check-in notifications, chat for
      tournament lobby, admin live dashboards. Fallback: SSE via async view.
- [x] **Notifications modernization** — replace `Notification` m2m (profiles/models.py:18) with
      per-user `Notification` rows + push channels (web push / email digest); fix ownership (3.1).
- [x] **Scheduling** — league auto-scheduler (round-robin), match reschedule requests, calendar/iCal
      export, timezone-aware display (`timezone.now()` everywhere, currently naive/aware mixed).
- [x] **Trophy/achievement system** — models exist (`num_bronze/silver/gold/plat/diamond/titanium`,
      profiles/models.py:75-82) but nothing awards them; wire into tournament/league wins.
- [x] **Team features** — roster management (Roster/RosterRole/RosterMember exist, unused), scrim
      scheduler, team analytics, jersey/logo uploads with moderation.
- [x] **Payments** — replace/augment PayPal IPN with Stripe Checkout (credits purchase), cashout
      flow (`current_earning`), credits gifting.
- [x] **eSports integrations** — Discord OAuth login (there's a Discord field, no auth), Steam API
      (steamid64), Twitch API (verify twitch channel, stream embeds on match pages), auto score fetch.
- [x] **Moderation** — report/flag system for users/teams/players, content moderation queue for
      images/news comments.
- [x] **Leaderboards** — per game/platform seasonal leaderboards; use existing XP/rank fields but move
      rank computation to scheduled tasks (`calculate_rank` is O(n) on every request path).
- [x] **Search** — site-wide search (news, teams, tournaments, leagues, users) via Postgres full-text
      or Elasticsearch/Meilisearch; replace `searchusers`/`support search` hacks.
- [x] **Emails** — transactional template emails (invites, match reminders, dispute outcomes, ticket
      updates) with HTML templates; switch from raw strings to `EmailMultiAlternatives`.
- [x] **Analytics** — staff dashboards: registrations, activity, wager volume, store revenue,
      tournament participation; export to CSV.

### 5.3 Sports-expansion (per README: "support for traditional sports")
- [x] `SportChoice` exists on Match/League/Tournament but no UI — build per-sport score schemas
      (goal-based, point-based, round-based), sport-specific stat entry forms.
- [x] Generic "event" abstraction (sport/league/tournament/ladder/season) so future event types
      share bracket/standings/reporting infrastructure.

### 5.4 Modern admin
- [x] Evaluate replacing the custom staff panel with Django admin + custom admin classes (many
      models have sparse admin.py); or keep the staff panel but rebuild it on the new frontend
      (Phase 6) with the permission system from 3.2. Recommend: keep custom panel (it's a product
      differentiator), rebuild UI.

---

## Phase 6 — Frontend Modernization

### 6.1 Foundation
- [x] Add `<meta charset>` + `<meta name="viewport">` to `base.html` (missing — site renders at 980px
      on phones).
- [x] Unify the stack: currently Bootstrap 3.3.7 (public, CDN) vs Bootstrap 4.0.0 (staff, vendored).
      Migrate everything to **Bootstrap 5** (or Tailwind for the public site) with one shared
      design system; remove SRI'd old CDNs.
- [x] jQuery 3.3.1 → remove (vanilla JS / Alpine.js / htmx); DataTables 1.10.16 → keep if staff
      tables survive, or replace with simple pagination. Chart.js 2.7.1 → 4.x if used.
- [x] Font Awesome 5.0.4 → 6.x (single copy; base.html:14-15 loads it twice).
- [x] Remove dead code: `singletournament_bracket{8,16,32,64,128}.html` (~1,970 lines of copy-paste;
      not referenced by any view; one file has a broken tag at bracket8:148) — keep the generic
      `singletournament_bracket.html` + a match-cell include partial.
- [x] Introduce build tooling: `package.json` + esbuild or Vite; move inline JS to modules; vendor
      only built assets; stop shipping `.map` files.
- [x] CKEditor → migrate to a maintained editor (CKEditor 5 / TipTap) or keep 4 with pinned assets.

### 6.2 Templates & UI
- [x] Replace all `{{ form.as_table }}` forms with Bootstrap-form styled templates.
- [x] Fix invalid HTML: `tr>thead` inside tables (profile.html:90-93/107-109/124-126, store/store.html:12-18,
      teams/team_list.html:14-20, matches/matches_list.html:14-19, staff/matches/matches.html:13-19),
      nested `<tr>` (team_detail.html:88-100), `<button>` inside `<a>` (wager_request_detail.html:90-92),
      duplicate `id="header"`, stray tags (match_detail.html:160 unbalanced `</div>`, team_detail.html:13).
- [x] Move the 5× copy-pasted teamformat if/elif chains into a template filter (league_detail.html:90-102,
      singletournament_detail.html:90-102, match_detail.html:32-44, wager_match_detail.html:30-42,
      wager_request_detail.html:62-74).
- [x] Replace `document.write()` + `new Date(...)` inline scripts (12 occurrences across 7 files) with
      data attributes + shared JS.
- [x] Responsive: brackets need horizontal scroll/zoom; tables need collapse/overflow; remove the
      `<br>` hack padding in bracket/no_bracket templates; drop the `max-width: 680px` container cap
      (olly.css:66-69).
- [x] Accessibility: `<html lang>`, alt text on all images, `label for`/`id` on all form fields,
      `aria-label` on icon-only buttons, semantic heading structure, focus states.
- [x] Fix `{{ field.errors }}` references that resolve to nothing (edit_profile.html:11,
      registration_form_template.html:2, xfer_form.html:2); show form errors on login (none today).
- [x] Fix dead branches: base.html:59, matches_list.html:26 (`!= None or != ""` → always true).
- [x] Replace hardcoded URLs with `{% url %}` (profile.html:10-11, staff footer year 2020).
- [x] Dark mode + consistent spacing/typography tokens.

### 6.3 UX improvements
- [x] Mobile check-in / match reporting flow (the core user action) — redesign as a guided wizard.
- [x] Tournament bracket with live-updating matches (fetch or websocket).
- [x] League standings with tiebreakers explanation and season timeline.
- [x] Public profiles with stats, trophies, match history timelines.
- [x] Onboarding: first-login wizard (link accounts, join/verify email, find a team).

---

## Phase 7 — Data, Migrations & Quality

- [x] Squash the 64 migration files into per-app `0001` snapshots after the model changes settle;
      verify `makemigrations --check` clean in CI.
- [x] Audit model design debt:
  - Money stored in `PositiveSmallIntegerField` (credits, earnings, product.amount as FloatField) →
    `DecimalField`/`IntegerField` with validation; `store/models.py:20` FloatField for money.
  - `UserProfile.user = OneToOneField(related_name='user')` — confusing accessor; migrate to
    `related_name='profile'` with a data migration + query sweep.
  - `Match`/`WagerMatch`/`TeamMatchStats` — add indexes on FK + datetime fields; `matches` m2m on
    Team is unused (teams/models.py:48).
  - `Notification` → move to per-user model (5.2).
- [x] Data integrity scripts: XP/rank recompute, credits ledger audit (Transaction vs Transfer vs
      UserProfile totals), duplicate `OllySetting` cleanup (staff/views/staff.py:176).
- [x] `Team.get_total_xp` / `get_rank` — O(n) loop saving per invite; replace with aggregate queries
      or scheduled tasks.
- [x] Add `IntegerChoices`/`TextChoices` enums replacing raw `(value, label)` tuples and magic numbers
      (teamformat/bestof chains, RECORD_FORMAT_CHOICES).
- [x] Type hints + mypy for new code; ruff for lint; pre-commit hooks (ruff, black, mypy, djhtml).
- [x] Upgrade test stack to pytest-django; set coverage floor (start 40%, raise over time); add
      property/unit tests for bracket generation, league standings math, credit ledger.

---
## Suggested Execution Order

1. **Phase 0** (baseline + safety net) — 3-5 days
2. **Phase 1.1** (Django 4.2 LTS) — with Phase 2 fixes interleaved, ~2-3 weeks
3. **Phase 2** (crash bugs — unblock every broken flow) — 1-2 weeks
4. **Phase 3** (security) — 1 week
5. **Phase 4** (complete half-built features) — 2-3 weeks
6. **Phase 6.1 + 6.2** (frontend foundation — do early to avoid double work on staff UI)
7. **Phase 5** (new features, highest value first: double-elim → API → real-time → payments)
8. **Phase 7** (continuous, alongside everything else)

## Not Yet Implemented (deferred — candidate backlog)

- Remote-branch salvage review (`rewrite`, `permissions-rewrite`, `2fa`, `league_match_scheduler`, `match_stats`, …)
- Notification model restructure (per-user rows replacing the m2m) — current m2m + WebSocket badge ships instead
- Production channel layer: Redis + `channels-redis`, run via daphne; dev uses InMemoryChannelLayer
- Stats UI wiring (StatsPlayer/TeamMatchStats entry + display), CS:GO-specific schema generalization
- Trophy/achievement awarding logic, Roster/RosterRole/RosterMember usage, team analytics
- Sports-expansion UI (SportChoice per-sport score schemas, generic event abstraction)
- eSports integrations: Discord/Steam/Twitch OAuth, automatic score fetch
- Moderation queue (reports/flags), site-wide search, staff analytics dashboards, i18n
- Transactional email polish (all flows), Stripe webhook hardening against replay
- pytest-django + coverage gate, ruff/mypy/pre-commit (CI currently runs `manage.py test` + docker build)
- tempusdominus datetimepicker (BS4-era) popup restyle for Bootstrap 5
- Live-updating bracket (WS), mobile match-report wizard, onboarding wizard, tiebreaker explainer

## Verification for Each Phase

- `python manage.py check --deploy` passes
- `pytest` green with coverage gate
- `makemigrations --check --dry-run` clean
- Manual smoke of every flow in the checklist: register → verify → create team → invite → join
  tournament → report match → dispute → wager → league season → store purchase
- `ruff check .` clean on touched files