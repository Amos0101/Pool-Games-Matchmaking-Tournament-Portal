from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.chat_list, name='chat_list'),
    path('room/<int:room_id>/', views.chat_room, name='chat_room'),
    path('start/<int:user_id>/', views.start_chat, name='start_chat'),
    path('api/unread-count/', views.get_unread_count, name='unread_count'),
    path('api/chat-list-updates/', views.get_chat_list_updates, name='chat_list_updates'),
    path('api/send-message/<int:room_id>/', views.send_message, name='send_message'),
    path('api/get-messages/<int:room_id>/', views.get_messages, name='get_messages'),
]
