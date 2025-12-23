from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from chat.models import Chat
from groupchat.models import GroupChat, GroupMessage
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        if user:
            # Create Django session
            login(request, user)

            # Create JWT token for API/WebSocket
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            # Optionally store token in cookie for frontend JS
            response = redirect('frontend-dashboard')
            response.set_cookie('access_token', access_token, httponly=False)
            return response
        else:
            return render(request, 'frontend/login.html', {'error': 'Invalid credentials'})

    return render(request, 'frontend/login.html')

def signup_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return render(request, 'frontend/signup.html', {'error': 'Passwords do not match'})

        if User.objects.filter(email=email).exists():
            return render(request, 'frontend/signup.html', {'error': 'Email already exists'})

        user = User.objects.create_user(username=email, email=email, password=password)
        user.save()

        # Log the user in after signup
        login(request, user)

        # Create JWT token
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        response = redirect('frontend-dashboard')
        response.set_cookie('access_token', access_token, httponly=False)
        return response

    return render(request, 'frontend/signup.html')

@login_required
def dashboard_view(request):
    return render(request, 'frontend/dashboard.html')

@login_required
def chat_list_view(request):
    return render(request, 'frontend/chat_list.html')

@login_required
def chat_view(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    if request.user not in chat.members.all():
        return redirect('frontend-dashboard')
    return render(request, 'frontend/chat.html', {'chat_id': chat_id})

@login_required
def group_list_view(request):
    return render(request, 'frontend/group_list.html')

@login_required
def group_chat_view(request, group_id):
    group = get_object_or_404(GroupChat, id=group_id)
    if not group.groupmember_set.filter(user=request.user).exists():
        return redirect('frontend-dashboard')
    messages = GroupMessage.objects.filter(group=group).order_by('timestamp')[:50]  # Last 50 messages
    return render(request, 'frontend/group_chat.html', {'group': group, 'messages': messages})

@login_required
def forgot_password_view(request):
    return render(request, 'frontend/forgot_password.html')
