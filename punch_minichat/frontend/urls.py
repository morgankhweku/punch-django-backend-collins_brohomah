from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='frontend-login'),
    path('signup/', views.signup_view, name='frontend-signup'),
    path('dashboard/', views.dashboard_view, name='frontend-dashboard'),
    path('chats/', views.chat_list_view, name='frontend-chat-list'),
    path('chat/<int:chat_id>/', views.chat_view, name='frontend-chat'),
    path('groups/', views.group_list_view, name='frontend-group-list'),
    path('group/<int:group_id>/', views.group_chat_view, name='frontend-group-chat'),
    path('forgot-password/', views.forgot_password_view, name='frontend-forgot-password'),
]
