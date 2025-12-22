from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json

class GroupChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """
        Called when a WebSocket connection is initiated.
        Authenticates user and joins the group if valid.
        """
        user = self.scope.get("user", None)
        print("Connecting user:", user)

        # Reject if no user or not authenticated
        if not user or not user.is_authenticated:
            await self.close()
            return

        # Get the group ID from URL kwargs
        self.group_id = self.scope['url_route']['kwargs']['group_id']
        self.group_name = f"group_{self.group_id}"

        # Join the group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()
        print(f"User {user.email} connected to group {self.group_name}")

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
        print(f"User disconnected from group {getattr(self, 'group_name', 'unknown')}")

    async def receive(self, text_data):
        """
        Called when a message is received from WebSocket.
        Broadcasts the message to all users in the group.
        """
        user = self.scope.get("user")
        if not user or not user.is_authenticated:
            await self.close()
            return

        try:
            data = json.loads(text_data)
            message = data.get("message", "").strip()
            if not message:
                return
        except json.JSONDecodeError:
            return  # Ignore invalid JSON

        # Broadcast message to group
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chat_message",
                "message": message,
                "user": user.email,
            }
        )

    async def chat_message(self, event):
        """
        Called when a message is sent to the group.
        Sends the message to the WebSocket client.
        """
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "user": event["user"]
        }))
