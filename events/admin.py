from django.contrib import admin
from .models import Event, EventView

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_date', 'location', 'entry_fee', 'max_participants', 'show_on_homepage', 'created_at']
    list_filter = ['event_date', 'show_on_homepage', 'created_at']
    search_fields = ['title', 'description', 'location']
    list_editable = ['show_on_homepage']
    date_hierarchy = 'event_date'
    ordering = ['event_date']

@admin.register(EventView)
class EventViewAdmin(admin.ModelAdmin):
    list_display = ['user', 'event', 'viewed_at']
    list_filter = ['viewed_at']
    search_fields = ['user__username', 'event__title']
    readonly_fields = ['viewed_at']
