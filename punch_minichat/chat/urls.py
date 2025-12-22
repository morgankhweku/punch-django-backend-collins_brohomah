from django.urls import path
from .views import CreateChatView, ListChatsView, ChatMessagesView

urlpatterns = [
    path("create", CreateChatView.as_view()),
    path("list", ListChatsView.as_view()),
    path("<int:chat_id>/messages", ChatMessagesView.as_view()),
]
