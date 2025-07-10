from django.urls import path
from . import views

app_name = 'matches'

urlpatterns = [
    path('create/', views.create_match, name='create_match'),
    path('my-matches/', views.my_matches, name='my_matches'),
    path('confirm/<int:match_id>/', views.confirm_match, name='confirm_match'),
    path('cancel/<int:match_id>/', views.cancel_match, name='cancel_match'),
    path('api/pending-count/', views.pending_matches_count_api, name='pending_matches_count_api'),
]
