from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.views.generic import View
# Create your views here.

def index(request):
    template_name = 'pages/index.html'
    return render(request, template_name)
    #return HttpResponse("TEST")
