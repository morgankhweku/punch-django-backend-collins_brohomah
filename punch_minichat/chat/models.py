from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Chat(models.Model):
    members = models.ManyToManyField(User, related_name="chats")
    is_group = models.BooleanField(default=False)
    name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        if self.is_group:
            return f"Group: {self.name}"
        return f"Chat between: {', '.join([u.username for u in self.members.all()])}"


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
