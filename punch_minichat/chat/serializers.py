from rest_framework import serializers
from .models import Chat, Message


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ("id", "user1", "user2", "created_at")


class MessageSerializer(serializers.ModelSerializer):
    sender_email = serializers.ReadOnlyField(source="sender.email")

    class Meta:
        model = Message
        fields = ("id", "chat", "sender_email", "content", "created_at")
