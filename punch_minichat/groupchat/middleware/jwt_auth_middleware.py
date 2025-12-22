from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from urllib.parse import parse_qs
import jwt
from django.conf import settings

User = get_user_model()

class JWTAuthMiddleware(BaseMiddleware):
    """
    Middleware for Django Channels to authenticate users using JWT in query string.
    """
    async def __call__(self, scope, receive, send):
        # Parse query string
        query_string = parse_qs(scope["query_string"].decode())
        token = query_string.get("token", [None])[0]

        scope["user"] = None

        if token:
            try:
                # Decode token
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                user_id = payload.get("user_id")
                if user_id:
                    # Fetch user from DB asynchronously
                    scope["user"] = await database_sync_to_async(User.objects.get)(id=user_id)
            except Exception as e:
                print("JWT error:", e)

        # Debug print
        print("Scope user after validation:", scope["user"])

        return await super().__call__(scope, receive, send)
