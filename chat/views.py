from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import ChatRoom, Message, UserStatus
import json

User = get_user_model()


@login_required
def chat_list(request):
    """Display list of chat rooms for the current user"""
    chat_rooms = ChatRoom.objects.filter(participants=request.user).prefetch_related('participants', 'messages')

    # Create UserStatus for current user if it doesn't exist
    user_status, created = UserStatus.objects.get_or_create(user=request.user)
    user_status.is_online = True
    user_status.last_seen = timezone.now()
    user_status.save()

    # Prepare chat rooms with other participant info and unread counts
    chat_rooms_with_participants = []
    for room in chat_rooms:
        other_participant = room.get_other_participant(request.user)
        unread_count = Message.objects.filter(
            chat_room=room,
            is_read=False
        ).exclude(sender=request.user).count()

        chat_rooms_with_participants.append({
            'room': room,
            'other_participant': other_participant,
            'unread_count': unread_count
        })

    return render(request, 'chat/chat_list.html', {
        'chat_rooms_with_participants': chat_rooms_with_participants
    })


@login_required
def chat_room(request, room_id):
    """Display a specific chat room"""
    chat_room = get_object_or_404(ChatRoom, id=room_id, participants=request.user)
    messages = chat_room.messages.all()[:50]  # Get last 50 messages
    other_participant = chat_room.get_other_participant(request.user)

    # Mark messages as read
    Message.objects.filter(chat_room=chat_room).exclude(sender=request.user).update(is_read=True)

    # Update user status
    user_status, created = UserStatus.objects.get_or_create(user=request.user)
    user_status.is_online = True
    user_status.last_seen = timezone.now()
    user_status.save()

    return render(request, 'chat/chat_room.html', {
        'chat_room': chat_room,
        'messages': messages,
        'other_participant': other_participant,
    })


@login_required
def start_chat(request, user_id):
    """Start a chat with another user"""
    if request.user.user_type != 'player':
        return redirect('accounts:player_directory')

    other_user = get_object_or_404(User, id=user_id, user_type='player')

    if other_user == request.user:
        return redirect('accounts:player_directory')

    # Check if chat room already exists
    existing_room = ChatRoom.objects.filter(
        participants=request.user
    ).filter(
        participants=other_user
    ).first()

    if existing_room:
        return redirect('chat:chat_room', room_id=existing_room.id)

    # Create new chat room
    chat_room = ChatRoom.objects.create()
    chat_room.participants.add(request.user, other_user)

    return redirect('chat:chat_room', room_id=chat_room.id)


@login_required
def get_unread_count(request):
    """Get unread message count for current user"""
    unread_count = Message.objects.filter(
        chat_room__participants=request.user,
        is_read=False
    ).exclude(sender=request.user).count()

    return JsonResponse({'unread_count': unread_count})


@login_required
def get_chat_list_updates(request):
    """Get updates for chat list including unread counts and last messages"""
    chat_rooms = ChatRoom.objects.filter(participants=request.user).prefetch_related('participants', 'messages')

    chat_updates = []
    for room in chat_rooms:
        other_participant = room.get_other_participant(request.user)
        unread_count = Message.objects.filter(
            chat_room=room,
            is_read=False
        ).exclude(sender=request.user).count()

        last_message = room.messages.first()

        chat_updates.append({
            'room_id': room.id,
            'other_participant_id': other_participant.id,
            'unread_count': unread_count,
            'last_message': {
                'content': last_message.content if last_message else '',
                'timestamp': last_message.timestamp.isoformat() if last_message else '',
                'sender_username': last_message.sender.username if last_message else ''
            } if last_message else None
        })

    return JsonResponse({'chat_updates': chat_updates})


@require_POST
@login_required
def send_message(request, room_id):
    """Send a message to a chat room"""
    chat_room = get_object_or_404(ChatRoom, id=room_id, participants=request.user)

    try:
        data = json.loads(request.body)
        message_content = data.get('message', '').strip()

        if not message_content:
            return JsonResponse({'success': False, 'error': 'Message cannot be empty'})

        # Create the message
        message = Message.objects.create(
            chat_room=chat_room,
            sender=request.user,
            content=message_content
        )

        # Update chat room timestamp
        chat_room.save()

        return JsonResponse({
            'success': True,
            'message': {
                'id': message.id,
                'content': message.content,
                'sender_id': message.sender.id,
                'sender_username': message.sender.username,
                'timestamp': message.timestamp.isoformat(),
                'formatted_time': message.timestamp.strftime('%H:%M')
            }
        })

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def get_messages(request, room_id):
    """Get messages for a chat room (for polling)"""
    chat_room = get_object_or_404(ChatRoom, id=room_id, participants=request.user)

    # Get the last message ID from the request
    last_message_id = request.GET.get('last_message_id', 0)

    # Get new messages since the last message ID
    messages = Message.objects.filter(
        chat_room=chat_room,
        id__gt=last_message_id
    ).order_by('timestamp')

    # Mark new messages as read (except own messages)
    Message.objects.filter(
        chat_room=chat_room,
        id__gt=last_message_id
    ).exclude(sender=request.user).update(is_read=True)

    # Prepare message data
    message_data = []
    for message in messages:
        message_data.append({
            'id': message.id,
            'content': message.content,
            'sender_id': message.sender.id,
            'sender_username': message.sender.username,
            'timestamp': message.timestamp.isoformat(),
            'formatted_time': message.timestamp.strftime('%H:%M')
        })

    # Get other participant's online status
    other_participant = chat_room.get_other_participant(request.user)
    other_status = UserStatus.objects.filter(user=other_participant).first()
    is_online = False
    if other_status:
        # Consider user online if they were active in the last 2 minutes
        time_diff = timezone.now() - other_status.last_seen
        is_online = other_status.is_online and time_diff.total_seconds() < 120

    return JsonResponse({
        'messages': message_data,
        'other_user_online': is_online
    })
