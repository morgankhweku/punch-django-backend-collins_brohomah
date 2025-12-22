from django.urls import path
from .views import CreateGroupChatView

urlpatterns = [
    path("create/", CreateGroupChatView.as_view()),
]
