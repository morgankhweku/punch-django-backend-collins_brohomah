from django.db.models import Q
from rest_framework.exceptions import ValidationError
from .models import Chat
from django.contrib.auth import get_user_model


User = get_user_model()

def get_or_create_chat(user_a, other_user_id):
    if user_a.id == other_user_id:
        raise ValidationError({"message": "Cannot chat with yourself"})
    
    try:
        user_b = User.objects.get(id=other_user_id)
    except User.DoesNotExist:
        raise ValidationError({"message": "User does not exist"})

    chat = Chat.objects.filter(
        Q(user1=user_a, user2=user_b) |
        Q(user1=user_b, user2=user_a)
    ).first()

    if chat:
        return chat

    return Chat.objects.create(user1=user_a, user2=user_b)
