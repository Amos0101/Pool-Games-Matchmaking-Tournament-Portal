import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import ChatRoom, Message, UserStatus

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'
        self.user = self.scope['user']
        self.user_group_name = f'user_{self.user.id}'

        print(f"WebSocket connect attempt for room {self.room_id} by user {self.user}")

        # Check if user is authenticated
        if not self.user.is_authenticated:
            print("User not authenticated, closing connection")
            await self.close()
            return

        # Verify user has access to this chat room
        has_access = await self.check_room_access()
        if not has_access:
            print(f"User {self.user} doesn't have access to room {self.room_id}")
            await self.close()
            return

        # Join room group and user group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.channel_layer.group_add(
            self.user_group_name,
            self.channel_name
        )

        print(f"User {self.user} connected to room {self.room_id}")
        await self.accept()

        # Update user status to online
        await self.update_user_status(True)

        # Notify others that user is online
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_status',
                'user_id': self.user.id,
                'username': self.user.username,
                'is_online': True
            }
        )

    async def disconnect(self, close_code):
        print(f"WebSocket disconnect for room {self.room_id} by user {self.user}")

        # Update user status to offline
        if hasattr(self, 'user') and self.user.is_authenticated:
            await self.update_user_status(False)

            # Notify others that user is offline
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_status',
                    'user_id': self.user.id,
                    'username': self.user.username,
                    'is_online': False
                }
            )

        # Leave room group and user group
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

        if hasattr(self, 'user_group_name'):
            await self.channel_layer.group_discard(
                self.user_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message_content = text_data_json.get('message', '').strip()

            if not message_content:
                return

            print(f"Received message from {self.user}: {message_content}")

            # Save message to database
            message = await self.save_message(message_content)

            # Get other participant for notifications
            other_participant = await self.get_other_participant()

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message_content,
                    'username': self.user.username,
                    'user_id': self.user.id,
                    'timestamp': message.timestamp.isoformat(),
                    'message_id': message.id
                }
            )

            # Send notification update to other participant's user group
            if other_participant:
                await self.channel_layer.group_send(
                    f'user_{other_participant.id}',
                    {
                        'type': 'notification_update',
                        'room_id': self.room_id,
                        'sender_username': self.user.username,
                        'message_preview': message_content[:50],
                        'timestamp': message.timestamp.isoformat()
                    }
                )

        except json.JSONDecodeError:
            print("Invalid JSON received")
        except Exception as e:
            print(f"Error in receive: {e}")

    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message': event['message'],
            'username': event['username'],
            'user_id': event['user_id'],
            'timestamp': event['timestamp'],
            'message_id': event['message_id']
        }))

    async def user_status(self, event):
        # Send user status update to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'user_status',
            'user_id': event['user_id'],
            'username': event['username'],
            'is_online': event['is_online']
        }))

    async def notification_update(self, event):
        # Send notification update to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'notification_update',
            'room_id': event['room_id'],
            'sender_username': event['sender_username'],
            'message_preview': event['message_preview'],
            'timestamp': event['timestamp']
        }))

    @database_sync_to_async
    def check_room_access(self):
        try:
            chat_room = ChatRoom.objects.get(id=self.room_id)
            return chat_room.participants.filter(id=self.user.id).exists()
        except ChatRoom.DoesNotExist:
            return False

    @database_sync_to_async
    def get_other_participant(self):
        try:
            chat_room = ChatRoom.objects.get(id=self.room_id)
            return chat_room.get_other_participant(self.user)
        except ChatRoom.DoesNotExist:
            return None

    @database_sync_to_async
    def save_message(self, content):
        try:
            chat_room = ChatRoom.objects.get(id=self.room_id)
            message = Message.objects.create(
                chat_room=chat_room,
                sender=self.user,
                content=content
            )
            # Update chat room's updated_at timestamp
            chat_room.save()
            return message
        except Exception as e:
            print(f"Error saving message: {e}")
            raise

    @database_sync_to_async
    def update_user_status(self, is_online):
        try:
            user_status, created = UserStatus.objects.get_or_create(user=self.user)
            user_status.is_online = is_online
            user_status.save()
        except Exception as e:
            print(f"Error updating user status: {e}")
