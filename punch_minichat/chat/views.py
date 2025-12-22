from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import models

from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer
from .services import get_or_create_chat

class CreateChatView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        other_user_id = request.data.get("user_id")
        
        if not other_user_id:
            return Response(
                {"detail": "user_id is required"},
                status=400
            )


        chat = get_or_create_chat(request.user, other_user_id)
        serializer = ChatSerializer(chat)

        return Response({
            "chat": serializer.data
        })


class ListChatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # return { chats: [...] }
        chats = Chat.objects.filter(
            models.Q(user1=request.user) | models.Q(user2=request.user)
        )
        serializer = ChatSerializer(chats, many=True)
        return Response({
            "chats": serializer.data
        })

class ChatMessagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, chat_id):
        messages = Message.objects.filter(chat_id=chat_id)
        serializer = MessageSerializer(messages, many=True)
        return Response({ "messages": serializer.data })
