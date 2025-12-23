from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import GroupChat, GroupMember, GroupMessage

User = get_user_model()


class GroupChatTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username='user1', email='user1@example.com', password='pass123')
        self.user2 = User.objects.create_user(username='user2', email='user2@example.com', password='pass123')
        self.user3 = User.objects.create_user(username='user3', email='user3@example.com', password='pass123')

    def test_create_group_success(self):
        self.client.force_authenticate(user=self.user1)
        data = {
            'name': 'Test Group',
            'member_usernames': ['user2', 'user3']
        }
        response = self.client.post('/api/groupchat/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(GroupChat.objects.count(), 1)
        group = GroupChat.objects.first()
        self.assertEqual(group.name, 'Test Group')
        self.assertEqual(group.owner, self.user1)
        self.assertEqual(GroupMember.objects.filter(group=group).count(), 3)  # owner + 2 members

    def test_create_group_no_name(self):
        self.client.force_authenticate(user=self.user1)
        data = {'member_usernames': ['user2']}
        response = self.client.post('/api/groupchat/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Name is required', response.data['detail'])

    def test_create_group_invalid_member_usernames(self):
        self.client.force_authenticate(user=self.user1)
        data = {
            'name': 'Test Group',
            'member_usernames': ['invaliduser', 'user2']
        }
        response = self.client.post('/api/groupchat/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        group = GroupChat.objects.first()
        self.assertEqual(GroupMember.objects.filter(group=group).count(), 2)  # owner + user2

    def test_send_message_success(self):
        # Create group
        group = GroupChat.objects.create(name='Test Group', owner=self.user1)
        GroupMember.objects.create(user=self.user1, group=group, is_admin=True)
        GroupMember.objects.create(user=self.user2, group=group)

        self.client.force_authenticate(user=self.user1)
        data = {'content': 'Hello World'}
        response = self.client.post(f'/api/groupchat/{group.id}/send/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(GroupMessage.objects.count(), 1)
        message = GroupMessage.objects.first()
        self.assertEqual(message.content, 'Hello World')
        self.assertEqual(message.sender, self.user1)

    def test_send_message_not_member(self):
        group = GroupChat.objects.create(name='Test Group', owner=self.user1)
        GroupMember.objects.create(user=self.user1, group=group, is_admin=True)

        self.client.force_authenticate(user=self.user2)  # user2 is not a member
        data = {'content': 'Hello World'}
        response = self.client.post(f'/api/groupchat/{group.id}/send/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('Not a member of this group', response.data['detail'])

    def test_send_message_empty_content(self):
        group = GroupChat.objects.create(name='Test Group', owner=self.user1)
        GroupMember.objects.create(user=self.user1, group=group, is_admin=True)

        self.client.force_authenticate(user=self.user1)
        data = {'content': ''}
        response = self.client.post(f'/api/groupchat/{group.id}/send/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Content cannot be empty', response.data['detail'])

    def test_send_message_group_not_found(self):
        self.client.force_authenticate(user=self.user1)
        data = {'content': 'Hello World'}
        response = self.client.post('/api/groupchat/999/send/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('Group not found', response.data['detail'])

    def test_list_messages_success(self):
        group = GroupChat.objects.create(name='Test Group', owner=self.user1)
        GroupMember.objects.create(user=self.user1, group=group, is_admin=True)
        GroupMember.objects.create(user=self.user2, group=group)

        # Create messages
        GroupMessage.objects.create(group=group, sender=self.user1, content='Message 1')
        GroupMessage.objects.create(group=group, sender=self.user2, content='Message 2')

        self.client.force_authenticate(user=self.user1)
        response = self.client.get(f'/api/groupchat/{group.id}/message/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['content'], 'Message 1')
        self.assertEqual(response.data[1]['content'], 'Message 2')

    def test_list_messages_not_member(self):
        group = GroupChat.objects.create(name='Test Group', owner=self.user1)
        GroupMember.objects.create(user=self.user1, group=group, is_admin=True)

        self.client.force_authenticate(user=self.user2)  # not a member
        response = self.client.get(f'/api/groupchat/{group.id}/message/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('Not a member of this group', response.data['detail'])

    def test_list_messages_group_not_found(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get('/api/groupchat/999/message/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('Group not found', response.data['detail'])

    def test_list_groups_for_user(self):
        # Create groups
        group1 = GroupChat.objects.create(name='Group 1', owner=self.user1)
        group2 = GroupChat.objects.create(name='Group 2', owner=self.user2)
        group3 = GroupChat.objects.create(name='Group 3', owner=self.user3)

        # Add user1 to groups
        GroupMember.objects.create(user=self.user1, group=group1, is_admin=True)
        GroupMember.objects.create(user=self.user1, group=group2)

        self.client.force_authenticate(user=self.user1)
        response = self.client.get('/api/groupchat/list/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        group_names = [group['name'] for group in response.data]
        self.assertIn('Group 1', group_names)
        self.assertIn('Group 2', group_names)
        self.assertNotIn('Group 3', group_names)

    def test_unauthenticated_access(self):
        # Test all endpoints without authentication
        endpoints = [
            ('/api/groupchat/create/', 'post', {'name': 'Test'}),
            ('/api/groupchat/list/', 'get'),
            ('/api/groupchat/1/send/', 'post', {'content': 'Test'}),
            ('/api/groupchat/1/message/', 'get'),
        ]
        for url, method, *args in endpoints:
            data = args[0] if args else {}
            if method == 'post':
                response = self.client.post(url, data, format='json')
            else:
                response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
