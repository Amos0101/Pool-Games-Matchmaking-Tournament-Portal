from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_date = models.DateTimeField()
    location = models.CharField(max_length=200)
    entry_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    max_participants = models.IntegerField(default=50)
    poster = models.ImageField(upload_to='event_posters/', blank=True, null=True)
    show_on_homepage = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['event_date']

    def __str__(self):
        return self.title

    @property
    def is_upcoming(self):
        return self.event_date > timezone.now()


class EventView(models.Model):
    """Track which events each user has viewed to show new event notifications"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'event']

    def __str__(self):
        return f"{self.user.username} viewed {self.event.title}"
