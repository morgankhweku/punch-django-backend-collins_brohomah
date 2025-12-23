from django.urls import path
from .views import CreateGroupView, ListGroupsView, ListGroupMessagesView, SendGroupMessageView

urlpatterns = [
    path("create", CreateGroupView.as_view(), name="create-group"),
    path("list", ListGroupsView.as_view(), name="list-groups"),
    path("<int:group_id>/message", ListGroupMessagesView.as_view(), name="list-group-messages"),
    path("<int:group_id>/send", SendGroupMessageView.as_view(), name="send-group-message"),
]
