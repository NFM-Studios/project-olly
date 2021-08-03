from django.shortcuts import render, redirect

from matches.models import Match
from news.models import Post
from profiles.models import UserProfile
from singletournaments.models import SingleEliminationTournament
from teams.models import Team
from .models import StaticInfo, Partner, OllySetting, StaticPage
from django.shortcuts import get_object_or_404


def index(request):
    staticinfo = StaticInfo.objects.get(pk=1)
    teamlist = Team.objects.all().order_by('-id')[:5]
    playerlist = UserProfile.objects.all().order_by('-id')[:3]
    newslist = Post.objects.all().order_by('-id')[:3]
    matchlist = Match.objects.all().order_by('-id')[:3]
    tournament_list = SingleEliminationTournament.objects.filter(active=True).order_by('-id')[:8]

    return render(request, 'pages/index.html',
                  {'list': tournament_list, 'staticinfo': staticinfo,
                   'newslist': newslist, 'matchlist': matchlist,
                   'teamlist': teamlist, 'playerlist': playerlist})


def whats_new(request):
    olly = OllySetting.objects.get(pk=1)
    return render(request, 'pages/whatsnew.html', {'olly': olly})


def about(request):
    staticinfo = StaticInfo.objects.get(pk=1)
    return render(request, 'pages/about.html', {'staticinfo': staticinfo})


def partners_page(request):
    partners = Partner.objects.all()
    return render(request, 'pages/partners.html', {'partners': partners})


def terms(request):
    staticinfo = StaticInfo.objects.get(pk=1)
    return render(request, 'pages/terms.html', {'staticinfo': staticinfo})


def privacy(request):
    staticinfo = StaticInfo.objects.get(pk=1)
    return render(request, 'pages/privacy.html', {'staticinfo': staticinfo})


def notfound(request, exception):
    staticinfo = StaticInfo.objects.get(pk=1)
    return render(request, 'pages/404.html', {'staticinfo': staticinfo})


def static_page(request, slug):
    page = get_object_or_404(StaticPage, slug=slug)
    if page.redirects:
        return redirect(page.url)
    else:
        return render(request, 'pages/static.html', {'page': page})
