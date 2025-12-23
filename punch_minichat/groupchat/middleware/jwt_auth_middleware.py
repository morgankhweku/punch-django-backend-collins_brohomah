from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from urllib.parse import parse_qs
from rest_framework_simplejwt.authentication import JWTAuthentication

User = get_user_model()

class JWTAuthMiddleware(BaseMiddleware):
    """
    Middleware for Django Channels to authenticate users using JWT in query string.
    """
    async def __call__(self, scope, receive, send):
        # Get token from query string or cookies
        query_string = parse_qs(scope["query_string"].decode())
        token = query_string.get("token", [None])[0] or scope.get("cookies", {}).get("access_token")

        scope["user"] = None

        if token:
            try:
                # Use JWTAuthentication to validate the token
                validated_token = JWTAuthentication().get_validated_token(token)
                user = JWTAuthentication().get_user(validated_token)
                scope["user"] = user
            except Exception as e:
                print("JWT error:", e)

        # Debug print
        print("Scope user after validation:", scope["user"])

        return await super().__call__(scope, receive, send)
