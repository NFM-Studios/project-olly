from django.shortcuts import render
from .models import StaticInfo
from matches.models import Match
from teams.models import Team
from news.models import Post
from singletournaments.models import SingleEliminationTournament
# Create your views here.


def index(request):
    teams = Team.objects.all()
    matches = Match.objects.all()
    news = Post.objects.all()
    tournaments = SingleEliminationTournament.objects.all()
    return render(request, 'pages/index.html', {'teams': teams, 'matches': matches, 
        'news': news, 'tournaments': tournaments})


def about(request):
        staticinfo = StaticInfo.objects.get(pk=1)
        return render(request, 'pages/about.html', {'staticinfo': staticinfo})


def terms(request):
    staticinfo = StaticInfo.objects.get(pk=1)
    return render(request, 'pages/terms.html', {'staticinfo': staticinfo})


def privacy(request):
    staticinfo = StaticInfo.objects.get(pk=1)
    return render(request, 'pages/privacy.html', {'staticinfo': staticinfo})


def notfound(request):
    staticinfo = StaticInfo.objects.get(pk=1)
    return render(request, 'pages/404.html', {'staticinfo': staticinfo})
