from django.contrib import admin
from .models import Venue, Match

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'created_at')
    search_fields = ('name', 'address')

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('challenger', 'opponent', 'venue', 'match_date', 'status', 'bid_amount')
    list_filter = ('status', 'match_date', 'venue')
    search_fields = ('challenger__username', 'opponent__username')
