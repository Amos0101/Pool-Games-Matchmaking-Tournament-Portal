from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class ChatRoom(models.Model):
    """
    Represents a chat room between two players
    """
    participants = models.ManyToManyField(User, related_name='chat_rooms')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        participants_list = list(self.participants.all())
        if len(participants_list) >= 2:
            return f"Chat: {participants_list[0].username} & {participants_list[1].username}"
        return f"Chat Room {self.id}"

    @property
    def last_message(self):
        return self.messages.first()

    def get_other_participant(self, user):
        """Get the other participant in the chat (not the current user)"""
        return self.participants.exclude(id=user.id).first()


class Message(models.Model):
    """
    Represents a message in a chat room
    """
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.sender.username}: {self.content[:50]}..."


class UserStatus(models.Model):
    """
    Track user online status
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='status')
    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {'Online' if self.is_online else 'Offline'}"
