from rest_framework import serializers
from .models import GroupChat


class GroupChatCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupChat
        fields = ["id", "name"]
