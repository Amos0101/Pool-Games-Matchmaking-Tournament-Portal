from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_date', 'location', 'show_on_homepage', 'created_at')
    list_filter = ('show_on_homepage', 'event_date')
    search_fields = ('title', 'description', 'location')
    list_editable = ('show_on_homepage',)
