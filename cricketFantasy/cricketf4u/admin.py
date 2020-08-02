from django.contrib import admin
from .models import UserInformation, League, Team, TeamLeagueLink

admin.site.register(UserInformation)
admin.site.register(League)
admin.site.register(Team)
admin.site.register(TeamLeagueLink)
# Register your models here.
