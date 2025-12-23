from django.shortcuts import render, get_object_or_404
from chat.models import Chat
from groupchat.models import GroupChat, GroupMessage

def login_view(request):
    return render(request, 'frontend/login.html')

def signup_view(request):
    return render(request, 'frontend/signup.html')

def dashboard_view(request):
    return render(request, 'frontend/dashboard.html')

def chat_list_view(request):
    return render(request, 'frontend/chat_list.html')

def chat_view(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    return render(request, 'frontend/chat.html', {'chat': chat})

def group_list_view(request):
    return render(request, 'frontend/group_list.html')

def group_chat_view(request, group_id):
    group = get_object_or_404(GroupChat, id=group_id)
    messages = GroupMessage.objects.filter(group=group).order_by('timestamp')[:50]  # Last 50 messages
    return render(request, 'frontend/group_chat.html', {'group': group, 'messages': messages})

def forgot_password_view(request):
    return render(request, 'frontend/forgot_password.html')
