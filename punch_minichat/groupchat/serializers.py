from rest_framework import serializers
from .models import GroupChat, GroupMember, GroupMessage
from django.contrib.auth import get_user_model
from django.utils.timesince import timesince

User = get_user_model()

class GroupChatSerializer(serializers.ModelSerializer):
    member_usernames = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=True
    )

    class Meta:
        model = GroupChat
        fields = ('id', 'name', 'created_at', 'member_usernames')

    def create(self, validated_data):
        member_usernames = validated_data.pop('member_usernames')
        group = super().create(validated_data)
        for username in member_usernames:
            try:
                user = User.objects.get(username=username)
                GroupMember.objects.create(user=user, group=group)
            except User.DoesNotExist:
                pass  # Skip invalid usernames
        return group

class GroupMessageSerializer(serializers.ModelSerializer):
    sender = serializers.ReadOnlyField(source='sender.email')
    timestamp = serializers.DateTimeField(source='created_at', read_only=True)

    class Meta:
        model = GroupMessage
        fields = ('id', 'group', 'sender', 'content', 'timestamp')
