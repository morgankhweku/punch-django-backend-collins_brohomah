from rest_framework import serializers
from .models import Chat, Message

class ChatSerializer(serializers.ModelSerializer):
    members = serializers.StringRelatedField(many=True)
    display_name = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = ['id', 'members', 'is_group', 'name', 'display_name']

    def get_display_name(self, obj):
        request = self.context.get('request')
        if request and not obj.is_group:
            current_user = request.user
            other_members = obj.members.exclude(id=current_user.id)
            if other_members.exists():
                return other_members.first().username
        return obj.name or "Unknown Chat"


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField()
    timestamp = serializers.DateTimeField(source='created_at', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'chat', 'sender', 'text', 'created_at', 'timestamp']
