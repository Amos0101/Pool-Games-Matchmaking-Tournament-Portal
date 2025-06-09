#!/usr/bin/env python
"""
Database setup script for Pool Games Portal
Run this script to create initial data for the application
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pool_portal.settings')
django.setup()

from django.contrib.auth import get_user_model
from matches.models import Venue
from events.models import Event
from accounts.models import PlayerProfile, RefereeProfile
from django.utils import timezone
from datetime import datetime, timedelta

User = get_user_model()

def create_sample_data():
    print("Creating sample data for Pool Games Portal...")
    
    # Create admin user
    if not User.objects.filter(username='admin').exists():
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@poolportal.com',
            password='admin123',
            first_name='Admin',
            last_name='User',
            user_type='player',
            location='System'
        )
        print("✓ Admin user created (username: admin, password: admin123)")
    
    # Create sample venues
    venues_data = [
        {
            'name': 'Downtown Pool Hall',
            'address': '123 Main St, Downtown',
            'description': 'Premier pool hall with 12 professional tables'
        },
        {
            'name': 'Sports Bar & Billiards',
            'address': '456 Oak Ave, Midtown',
            'description': 'Casual atmosphere with 8 pool tables and full bar'
        },
        {
            'name': 'Elite Billiards Club',
            'address': '789 Pine St, Uptown',
            'description': 'High-end club with tournament-quality tables'
        },
        {
            'name': 'Community Center Pool Room',
            'address': '321 Elm St, Suburbs',
            'description': 'Affordable community space with 6 tables'
        }
    ]
    
    for venue_data in venues_data:
        venue, created = Venue.objects.get_or_create(
            name=venue_data['name'],
            defaults=venue_data
        )
        if created:
            print(f"✓ Created venue: {venue.name}")
    
    # Create sample players
    players_data = [
        {
            'username': 'poolshark_mike',
            'email': 'mike@example.com',
            'first_name': 'Mike',
            'last_name': 'Johnson',
            'location': 'Downtown',
            'skill_level': 'advanced',
            'bio': 'Been playing pool for 15 years. Love 8-ball and 9-ball games.'
        },
        {
            'username': 'sarah_cue',
            'email': 'sarah@example.com',
            'first_name': 'Sarah',
            'last_name': 'Williams',
            'location': 'Midtown',
            'skill_level': 'intermediate',
            'bio': 'Casual player looking to improve my game and meet new people.'
        },
        {
            'username': 'rack_master',
            'email': 'david@example.com',
            'first_name': 'David',
            'last_name': 'Chen',
            'location': 'Uptown',
            'skill_level': 'professional',
            'bio': 'Tournament player with multiple local championships.'
        },
        {
            'username': 'jenny_breaks',
            'email': 'jenny@example.com',
            'first_name': 'Jenny',
            'last_name': 'Rodriguez',
            'location': 'Suburbs',
            'skill_level': 'beginner',
            'bio': 'New to pool but eager to learn and practice!'
        }
    ]
    
    for player_data in players_data:
        if not User.objects.filter(username=player_data['username']).exists():
            user = User.objects.create_user(
                username=player_data['username'],
                email=player_data['email'],
                password='password123',
                first_name=player_data['first_name'],
                last_name=player_data['last_name'],
                user_type='player',
                location=player_data['location']
            )
            
            PlayerProfile.objects.create(
                user=user,
                skill_level=player_data['skill_level'],
                bio=player_data['bio']
            )
            print(f"✓ Created player: {user.username}")
    
    # Create sample referees
    referees_data = [
        {
            'username': 'ref_tom',
            'email': 'tom@example.com',
            'first_name': 'Tom',
            'last_name': 'Anderson',
            'location': 'Downtown',
            'experience_years': 8,
            'certification': 'WPA Certified Referee'
        },
        {
            'username': 'ref_lisa',
            'email': 'lisa@example.com',
            'first_name': 'Lisa',
            'last_name': 'Brown',
            'location': 'Midtown',
            'experience_years': 5,
            'certification': 'Local League Certified'
        }
    ]
    
    for ref_data in referees_data:
        if not User.objects.filter(username=ref_data['username']).exists():
            user = User.objects.create_user(
                username=ref_data['username'],
                email=ref_data['email'],
                password='password123',
                first_name=ref_data['first_name'],
                last_name=ref_data['last_name'],
                user_type='referee',
                location=ref_data['location']
            )
            
            RefereeProfile.objects.create(
                user=user,
                experience_years=ref_data['experience_years'],
                certification=ref_data['certification']
            )
            print(f"✓ Created referee: {user.username}")
    
    # Create sample events
    events_data = [
        {
            'title': 'Monthly 8-Ball Tournament',
            'description': 'Join us for our monthly 8-ball tournament! Entry fee $20, winner takes $200 prize pool.',
            'event_date': timezone.now() + timedelta(days=15),
            'location': 'Downtown Pool Hall',
            'show_on_homepage': True
        },
        {
            'title': 'Beginner\'s Workshop',
            'description': 'Learn the basics of pool from professional instructors. Perfect for new players!',
            'event_date': timezone.now() + timedelta(days=7),
            'location': 'Community Center Pool Room',
            'show_on_homepage': True
        },
        {
            'title': 'Ladies Night Pool League',
            'description': 'Weekly ladies-only pool league. All skill levels welcome!',
            'event_date': timezone.now() + timedelta(days=3),
            'location': 'Sports Bar & Billiards',
            'show_on_homepage': False
        },
        {
            'title': 'Championship Qualifier',
            'description': 'Qualify for the regional championship. Advanced players only.',
            'event_date': timezone.now() + timedelta(days=30),
            'location': 'Elite Billiards Club',
            'show_on_homepage': True
        }
    ]
    
    for event_data in events_data:
        event, created = Event.objects.get_or_create(
            title=event_data['title'],
            defaults=event_data
        )
        if created:
            print(f"✓ Created event: {event.title}")
    
    print("\n🎉 Sample data creation completed!")
    print("\nYou can now:")
    print("- Login as admin (username: admin, password: admin123)")
    print("- Login as any player (password: password123)")
    print("- Browse players, create matches, and view events")
    print("\nSample player accounts:")
    for player in players_data:
        print(f"  - {player['username']} ({player['first_name']} {player['last_name']})")

if __name__ == '__main__':
    create_sample_data()
