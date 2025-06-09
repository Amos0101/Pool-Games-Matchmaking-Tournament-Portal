from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Venue(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Match(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Confirmation'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    challenger = models.ForeignKey(User, on_delete=models.CASCADE, related_name='challenged_matches')
    opponent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='opponent_matches')
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    match_date = models.DateField()
    match_time = models.TimeField()
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.challenger.username} vs {self.opponent.username} - {self.match_date}"
