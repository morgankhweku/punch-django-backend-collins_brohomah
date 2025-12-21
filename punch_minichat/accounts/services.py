from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

User = get_user_model()


def authenticate_user(email, password):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return None

    if not check_password(password, user.password):
        return None

    return user
