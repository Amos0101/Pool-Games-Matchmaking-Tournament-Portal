from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Max
from .models import ChatRoom, Message
from accounts.models import User


@login_required
def chat_list(request):
    if request.user.user_type != 'player':
        messages.error(request, 'Only players can access chat.')
        return redirect('events:home')

    # Get chat rooms for current user with latest message
    chat_rooms = ChatRoom.objects.filter(
        participants=request.user
    ).annotate(
        latest_message_time=Max('messages__timestamp')
    ).order_by('-latest_message_time')

    # Get latest message for each room
    for room in chat_rooms:
        room.latest_message = room.messages.order_by('-timestamp').first()
        room.unread_count = room.messages.filter(
            is_read=False
        ).exclude(sender=request.user).count()

    return render(request, 'chat/chat_list.html', {'chat_rooms': chat_rooms})


@login_required
def chat_room(request, room_id):
    if request.user.user_type != 'player':
        messages.error(request, 'Only players can access chat.')
        return redirect('events:home')

    room = get_object_or_404(ChatRoom, id=room_id, participants=request.user)

    # Mark messages as read
    Message.objects.filter(
        chat_room=room,
        is_read=False
    ).exclude(sender=request.user).update(is_read=True)

    # Get other participant
    other_participant = room.participants.exclude(id=request.user.id).first()

    return render(request, 'chat/chat_room.html', {
        'room': room,
        'other_participant': other_participant
    })


@login_required
def start_chat(request, user_id):
    if request.user.user_type != 'player':
        messages.error(request, 'Only players can access chat.')
        return redirect('events:home')

    other_user = get_object_or_404(User, id=user_id, user_type='player')

    if other_user == request.user:
        messages.error(request, 'You cannot chat with yourself.')
        return redirect('accounts:player_directory')

    # Find existing chat room or create new one
    existing_room = ChatRoom.objects.filter(
        participants=request.user
    ).filter(
        participants=other_user
    ).first()

    if existing_room:
        return redirect('chat:chat_room', room_id=existing_room.id)
    else:
        # Create new chat room
        room = ChatRoom.objects.create()
        room.participants.add(request.user, other_user)
        return redirect('chat:chat_room', room_id=room.id)


@login_required
def unread_messages_count_api(request):
    """API endpoint to get unread messages count for current user"""
    if request.user.user_type != 'player':
        return JsonResponse({'unread_count': 0})

    unread_count = Message.objects.filter(
        chat_room__participants=request.user,
        is_read=False
    ).exclude(sender=request.user).count()

    return JsonResponse({'unread_count': unread_count})
