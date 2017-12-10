from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.views.generic import View
from .models import StaticInfo
# Create your views here.

def index(request):
    return render(request, 'pages/index.html')

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
