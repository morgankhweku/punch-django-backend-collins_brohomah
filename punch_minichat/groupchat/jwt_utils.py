import jwt
from django.conf import settings
import datetime

def create_jwt_for_user(user):
    payload = {
        "user_id": user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        "iat": datetime.datetime.utcnow()
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return token
