from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    template_name = 'pages/index.html;'
    return render(request, template_name)
    #return HttpResponse("TEST")
