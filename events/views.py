from django.shortcuts import render
from django.views.generic import ListView
from django.utils import timezone
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Event, EventView


class HomeView(ListView):
    model = Event
    template_name = 'home.html'
    context_object_name = 'featured_events'

    def get_queryset(self):
        # Show only future events that are marked for homepage
        return Event.objects.filter(
            show_on_homepage=True,
            event_date__gte=timezone.now()
        )[:3]  # Show only 3 events on homepage

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add additional context for logged-in users
        if self.request.user.is_authenticated and self.request.user.user_type == 'player':
            from matches.models import Match
            from chat.models import Message

            # Get recent matches
            recent_matches = Match.objects.filter(
                Q(challenger=self.request.user) | Q(opponent=self.request.user)
            ).select_related('challenger', 'opponent', 'venue').order_by('-created_at')[:5]

            # Get pending matches count (matches sent TO this user)
            pending_matches_count = Match.objects.filter(
                opponent=self.request.user,
                status='pending'
            ).count()

            # Get unread messages count
            unread_messages = Message.objects.filter(
                chat_room__participants=self.request.user,
                is_read=False
            ).exclude(sender=self.request.user).count()

            # Get new events count (events created after user's last view)
            viewed_events = EventView.objects.filter(user=self.request.user).values_list('event_id', flat=True)
            new_events_count = Event.objects.filter(
                event_date__gte=timezone.now()
            ).exclude(id__in=viewed_events).count()

            # Calculate user stats
            total_matches = recent_matches.count()
            wins = 0  # This would be calculated based on match results when implemented

            context.update({
                'recent_matches': recent_matches,
                'pending_matches_count': pending_matches_count,
                'unread_messages': unread_messages,
                'new_events_count': new_events_count,
                'user_stats': {
                    'total_matches': total_matches,
                    'wins': wins,
                }
            })

        return context


class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    paginate_by = 9

    def get_queryset(self):
        # Show only future events
        return Event.objects.filter(event_date__gte=timezone.now())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Mark events as viewed for logged-in users
        if self.request.user.is_authenticated:
            events = context['events']
            for event in events:
                EventView.objects.get_or_create(
                    user=self.request.user,
                    event=event
                )

        return context


@login_required
def new_events_count_api(request):
    """API endpoint to get count of new events for the current user"""
    if request.user.user_type != 'player':
        return JsonResponse({'new_count': 0})

    # Get events that the user hasn't viewed yet
    viewed_events = EventView.objects.filter(user=request.user).values_list('event_id', flat=True)
    new_count = Event.objects.filter(
        event_date__gte=timezone.now()
    ).exclude(id__in=viewed_events).count()

    return JsonResponse({'new_count': new_count})
