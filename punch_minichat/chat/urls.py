from django.urls import path
from .views import CreateChatView, SendMessageView, ListChatsView, ListMessagesView

urlpatterns = [
    path("create", CreateChatView.as_view(), name="create-chat"),
    path("list/", ListChatsView.as_view(), name="list-chats"),
    path("<int:chat_id>/message", ListMessagesView.as_view(), name="list-messages"),
    path("<int:chat_id>/send", SendMessageView.as_view(), name="send-message"),
]
