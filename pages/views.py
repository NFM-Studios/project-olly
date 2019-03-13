from django.shortcuts import render

from matches.models import Match
from news.models import Post
from profiles.models import UserProfile
from singletournaments.models import SingleEliminationTournament
from teams.models import Team
from .models import StaticInfo, Partner


def index(request):
    # tournament_list = tournaments.reverse()[:4]
    # matchlist = matches.reverse()[:5]
    # teamlist = teams.reverse()[:5]
    staticinfo = StaticInfo.objects.get(pk=1)
    if request.tenant == 'online':
        teamlist = Team.objects.all().order_by('-id')[:5]
        matchlist = Match.objects.all().order_by('-id')[:4]
        newslist = Post.objects.all().order_by('-id')[:2]
        playerlist = UserProfile.objects.all().order_by('-id')[:3]
        tournament_list = SingleEliminationTournament.objects.filter(active=True).order_by('-id')[:6]
    elif request.tenant == 'binge':
        teamlist = Team.objects.all().order_by('-id')[:5]
        matchlist = Match.objects.all().order_by('-id')[:5]
        newslist = Post.objects.all().order_by('-id')[:2]
        tournament_list = SingleEliminationTournament.objects.filter(active=True).order_by('-id')[:4]
        playerlist = UserProfile.objects.all().order_by('-xp')[:3]
    elif request.tenant == 'roc':
        teamlist = Team.objects.all().order_by('-id')[:5]
        playerlist = UserProfile.objects.all().order_by('-id')[:3]
        newslist = Post.objects.all().order_by('-id')[:3]
        matchlist = Match.objects.all().order_by('-id')[:3]
        tournament_list = SingleEliminationTournament.objects.filter(active=True).order_by('-id')[:8]
    elif request.tenant == 'cashout':
        teamlist = Team.objects.all().order_by('-id')[:1]
        playerlist = UserProfile.objects.all().order_by('-xp')[:10]
        newslist = Post.objects.all().order_by('-id')[:3]
        matchlist = Match.objects.all().order_by('-id')[:3]
        tournament_list = SingleEliminationTournament.objects.filter(active=True).order_by('-id')[:6]
    elif request.tenant == 'ga':
        teamlist = Team.objects.all().order_by('-id')[:1]
        playerlist = UserProfile.objects.all().order_by('-xp')[:1]
        newslist = Post.published.all().order_by('-id')[:3]
        matchlist = Match.objects.all().order_by('-id')[:1]
        tournament_list = SingleEliminationTournament.objects.filter(active=True).order_by('-id')[:1]
    else:
        teamlist = Team.objects.all().order_by('-id')[:5]
        playerlist = UserProfile.objects.all().order_by('-id')[:3]
        newslist = Post.objects.all().order_by('-id')[:3]
        matchlist = Match.objects.all().order_by('-id')[:3]
        tournament_list = SingleEliminationTournament.objects.filter(active=True).order_by('-id')[:8]

    return render(request, 'pages/' + request.tenant + '/index.html',
                  {'list': tournament_list, 'staticinfo': staticinfo,
                   'newslist': newslist, 'matchlist': matchlist,
                   'teamlist': teamlist, 'playerlist': playerlist})


def about(request):
    staticinfo = StaticInfo.objects.get(pk=1)
    return render(request, 'pages/' + request.tenant + '/about.html', {'staticinfo': staticinfo})


def partners_page(request):
    partners = Partner.objects.all()
    return render(request, 'pages/' + request.tenant + '/partners.html', {'partners': partners})


def terms(request):
    staticinfo = StaticInfo.objects.get(pk=1)
    return render(request, 'pages/' + request.tenant + '/terms.html', {'staticinfo': staticinfo})


def privacy(request):
    staticinfo = StaticInfo.objects.get(pk=1)
    return render(request, 'pages/' + request.tenant + '/privacy.html', {'staticinfo': staticinfo})


def notfound(request, exception):
    staticinfo = StaticInfo.objects.get(pk=1)
    return render(request, 'pages/' + request.tenant + '/404.html', {'staticinfo': staticinfo})
