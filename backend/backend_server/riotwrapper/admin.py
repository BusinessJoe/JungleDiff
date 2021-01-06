from django.contrib import admin

from .models import Summoner, Match, Timeline

admin.site.register([Summoner, Match, Timeline])
