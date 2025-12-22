from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model

from .models import GroupChat, GroupMember

User = get_user_model()


class CreateGroupChatView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        name = request.data.get("name")
        member_ids = request.data.get("member_ids", [])

        if not name:
            return Response(
                {"detail": "Group name is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        #  Create group
        group = GroupChat.objects.create(
            name=name,
            owner=request.user
        )

        #  Add creator as admin
        GroupMember.objects.create(
            group=group,
            user=request.user,
            is_admin=True
        )

        #  Add other members
        members = User.objects.filter(id__in=member_ids).exclude(id=request.user.id)

        GroupMember.objects.bulk_create([
            GroupMember(group=group, user=member)
            for member in members
        ])

        return Response(
            {
                "group_id": group.id,
                "name": group.name,
                "members_added": members.count() + 1
            },
            status=status.HTTP_201_CREATED
        )
