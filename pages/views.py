from django.shortcuts import render
from .models import StaticInfo, Partner
from matches.models import Match
from teams.models import Team
from news.models import Post
from singletournaments.models import SingleEliminationTournament


def index(request):
    teamlist = Team.objects.all().order_by('-id')[:5]
    matchlist = Match.objects.all().order_by('-id')[:5]
    tournament_list = SingleEliminationTournament.objects.filter(active=True).order_by('-id')[:4]
    #tournament_list = tournaments.reverse()[:4]
    newslist = Post.objects.all().order_by('-id')[:3]
    #matchlist = matches.reverse()[:5]
    #teamlist = teams.reverse()[:5]
    staticinfo = StaticInfo.objects.get(pk=1)

    return render(request, 'pages/' + request.tenant + '/index.html', {'list': tournament_list, 'staticinfo': staticinfo,
                                                                       'newslist': newslist, 'matchlist': matchlist,
                                                                       'teamlist': teamlist})


def about(request):
        staticinfo = StaticInfo.objects.get(pk=1)
        return render(request, 'pages/' + request.tenant + '/about.html', {'staticinfo': staticinfo})


def partners_page(request):

    partners = Partner.objects.all()
    return render(request,  'pages/' + request.tenant + '/partners.html', {'partners': partners})


def terms(request):
    staticinfo = StaticInfo.objects.get(pk=1)
    return render(request, 'pages/' + request.tenant + '/terms.html', {'staticinfo': staticinfo})


def privacy(request):
    staticinfo = StaticInfo.objects.get(pk=1)
    return render(request, 'pages/' + request.tenant + '/privacy.html', {'staticinfo': staticinfo})


def notfound(request):
    staticinfo = StaticInfo.objects.get(pk=1)
    return render(request, 'pages/' + request.tenant + '/404.html', {'staticinfo': staticinfo})
