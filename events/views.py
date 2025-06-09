from django.shortcuts import render
from django.views.generic import ListView
from django.utils import timezone
from .models import Event

class HomeView(ListView):
    model = Event
    template_name = 'home.html'
    context_object_name = 'featured_events'
    
    def get_queryset(self):

        return Event.objects.filter(
            show_on_homepage=True,
            event_date__gte=timezone.now()
        )[:3]

class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    paginate_by = 9
    
    def get_queryset(self):

        return Event.objects.filter(event_date__gte=timezone.now())
