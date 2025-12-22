import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Chat, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
        self.room_group_name = f"chat_{self.chat_id}"

        user = self.scope.get("user")

        if not user or not user.is_authenticated:
            await self.close()
            return

        is_member = await self.is_chat_member(user, self.chat_id)
        if not is_member:
            await self.close()
            return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        if not text_data:
            return

        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            return

        message_text = data.get("message")
        if not message_text:
            return

        user = self.scope["user"]

        message = await self.save_message(user, self.chat_id, message_text)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message.content,
                "sender": user.email,
                "created_at": message.created_at.isoformat(),
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def is_chat_member(self, user, chat_id):
        return Chat.objects.filter(id=chat_id, members=user).exists()

    @database_sync_to_async
    def save_message(self, user, chat_id, content):
        chat = Chat.objects.get(id=chat_id)
        return Message.objects.create(
            chat=chat,
            sender=user,
            content=content
        )
