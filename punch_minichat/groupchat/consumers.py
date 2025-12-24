from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json
from .models import GroupChat, GroupMember, GroupMessage
from django.utils.timesince import timesince

class GroupChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """
        Called when a WebSocket connection is initiated.
        Authenticates user and joins the group if valid.
        """
        user = self.scope.get("user", None)

        # Reject if no user or not authenticated
        if not user or not user.is_authenticated:
            await self.close()
            return

        # Get the group ID from URL kwargs
        self.group_id = self.scope['url_route']['kwargs']['group_id']
        self.group_name = f"group_{self.group_id}"

        # Check if user is member
        is_member = await self.is_group_member(user, self.group_id)
        if not is_member:
            await self.close()
            return

        # Join the group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        """
        Called when WebSocket disconnects.
        Removes the user from the group.
        """
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        """
        Called when a message is received from WebSocket.
        Saves the message and broadcasts it to all users in the group.
        """
        user = self.scope.get("user")
        if not user or not user.is_authenticated:
            await self.close()
            return

        try:
            data = json.loads(text_data)
            message_text = data.get("message", "").strip()
            if not message_text:
                return
        except json.JSONDecodeError:
            return  # Ignore invalid JSON

        # Save the message
        saved_message = await self.save_message(user, self.group_id, message_text)

        # Broadcast message to group
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chat_message",
                "message": saved_message.content,
                "sender": user.username,
                "timestamp": saved_message.timestamp.isoformat(),
            }
        )

    async def chat_message(self, event):
        """
        Called when a message is sent to the group.
        Sends the message to the WebSocket client.
        """
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender": event["sender"],
            "timestamp": event["timestamp"]
        }))

    @database_sync_to_async
    def is_group_member(self, user, group_id):
        return GroupMember.objects.filter(group_id=group_id, user=user).exists()

    @database_sync_to_async
    def save_message(self, user, group_id, content):
        group = GroupChat.objects.get(id=group_id)
        return GroupMessage.objects.create(
            group=group,
            sender=user,
            content=content
        )
