from django.contrib import admin
from django.conf.urls import url, include
from .models import Match, MatchReport

admin.site.register(Match)
