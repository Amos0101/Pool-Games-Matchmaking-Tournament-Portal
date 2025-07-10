from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('events/', views.EventListView.as_view(), name='event_list'),
    path('api/new-count/', views.new_events_count_api, name='new_events_count_api'),
]
