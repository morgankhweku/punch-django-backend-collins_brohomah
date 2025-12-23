from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer
from groupchat.models import GroupChat
from groupchat.serializers import GroupChatSerializer

User = get_user_model()


# Utility function to get or create a one-on-one chat
def get_or_create_chat(user1, user2):
    chat = Chat.objects.filter(members=user1).filter(members=user2).first()
    if not chat:
        chat = Chat.objects.create()
        chat.members.add(user1, user2)
    return chat


# --------------------
# Create one-on-one chat by username
# --------------------
class CreateChatView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        other_username = request.data.get("username")
        if not other_username:
            return Response({"detail": "Username is required"}, status=400)

        try:
            other_user = User.objects.get(username=other_username)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=404)

        chat = get_or_create_chat(request.user, other_user)
        serializer = ChatSerializer(chat)
        return Response({
            "chat": serializer.data,
            "members": [u.username for u in chat.members.all()]  # frontend can use this
        })


# --------------------
# Send message in a chat
# --------------------
class SendMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, chat_id):
        try:
            chat = Chat.objects.get(id=chat_id)
        except Chat.DoesNotExist:
            return Response({"detail": "Chat not found"}, status=404)

        if request.user not in chat.members.all():
            return Response({"detail": "Not a member of this chat"}, status=403)

        message_text = request.data.get("message")
        if not message_text:
            return Response({"detail": "Message cannot be empty"}, status=400)

        message = Message.objects.create(
            chat=chat,
            sender=request.user,
            text=message_text
        )
        serializer = MessageSerializer(message)
        return Response(serializer.data)


# --------------------
# List messages in a chat
# --------------------
class ListMessagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, chat_id):
        try:
            chat = Chat.objects.get(id=chat_id)
        except Chat.DoesNotExist:
            return Response({"detail": "Chat not found"}, status=404)

        if request.user not in chat.members.all():
            return Response({"detail": "Not a member of this chat"}, status=403)

        messages = Message.objects.filter(chat=chat).order_by('created_at')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


# --------------------
# List all chats for a user
# --------------------
class ListChatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        chats = Chat.objects.filter(members=request.user).distinct()
        serializer = ChatSerializer(chats, many=True, context={'request': request})
        return Response(serializer.data)
