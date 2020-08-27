from django.contrib import admin

from .models import Team, TeamInvite

# Register your models here.
admin.site.register(Team)
admin.site.register(TeamInvite)