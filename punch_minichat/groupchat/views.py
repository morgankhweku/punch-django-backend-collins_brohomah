from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser
from django.contrib.auth import get_user_model
from .models import GroupChat, GroupMember, GroupMessage
from .serializers import GroupChatSerializer, GroupMessageSerializer

User = get_user_model()


# --------------------
# Create group chat
# --------------------
class CreateGroupView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        name = request.data.get("name")
        member_usernames = request.data.get("member_usernames", [])

        if not name:
            return Response({"detail": "Name is required"}, status=400)

        if not isinstance(member_usernames, list):
            return Response({"detail": "member_usernames must be a list"}, status=400)

        group = GroupChat.objects.create(name=name, owner=request.user)
        # Add owner as admin
        GroupMember.objects.create(user=request.user, group=group, is_admin=True)
        # Add other members
        for username in member_usernames:
            try:
                user = User.objects.get(username=username)
                GroupMember.objects.create(user=user, group=group)
            except User.DoesNotExist:
                pass  # Skip invalid usernames

        serializer = GroupChatSerializer(group)
        return Response(serializer.data)


# --------------------
# Send message in a group
# --------------------
class SendGroupMessageView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser]

    def post(self, request, group_id):
        try:
            group = GroupChat.objects.get(id=group_id)
        except GroupChat.DoesNotExist:
            return Response({"detail": "Group not found"}, status=404)

        if not GroupMember.objects.filter(group=group, user=request.user).exists():
            return Response({"detail": "Not a member of this group"}, status=403)

        content = request.data.get("content")
        if not content:
            return Response({"detail": "Content cannot be empty"}, status=400)

        message = GroupMessage.objects.create(
            group=group,
            sender=request.user,
            content=content
        )
        serializer = GroupMessageSerializer(message)
        return Response(serializer.data)


# --------------------
# List messages in a group
# --------------------
class ListGroupMessagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, group_id):
        print(f"ListGroupMessagesView: user={request.user}, group_id={group_id}")
        try:
            group = GroupChat.objects.get(id=group_id)
        except GroupChat.DoesNotExist:
            print(f"Group not found: {group_id}")
            return Response({"detail": "Group not found"}, status=404)

        is_member = GroupMember.objects.filter(group=group, user=request.user).exists()
        print(f"Is member: {is_member}")
        if not is_member:
            print(f"Not a member: user={request.user}, group={group}")
            return Response({"detail": "Not a member of this group"}, status=403)

        messages = GroupMessage.objects.filter(group=group).order_by('timestamp')
        print(f"Messages count: {messages.count()}")
        serializer = GroupMessageSerializer(messages, many=True)
        print(f"Serialized data: {serializer.data}")
        return Response(serializer.data)


# --------------------
# List all groups for a user
# --------------------
class ListGroupsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        groups = GroupChat.objects.filter(members__user=request.user).distinct()
        serializer = GroupChatSerializer(groups, many=True)
        return Response(serializer.data)
