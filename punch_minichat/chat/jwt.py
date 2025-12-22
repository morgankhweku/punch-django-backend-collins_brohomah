from urllib.parse import parse_qs
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from rest_framework_simplejwt.authentication import JWTAuthentication

@database_sync_to_async
def get_user_from_token(token):
    validated_token = JWTAuthentication().get_validated_token(token)
    user = JWTAuthentication().get_user(validated_token)
    return user

class JWTAuthMiddleware:
    """
    Custom middleware for authenticating WebSocket connections with JWT
    """

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        print("Query string received:", scope["query_string"].decode())
        print("User before validation:", scope.get("user"))

        query_string = parse_qs(scope["query_string"].decode())
        token_list = query_string.get("token")
        scope["user"] = AnonymousUser()

        if token_list:
            token = token_list[0]
            try:
                user = await get_user_from_token(token)
                scope["user"] = user or AnonymousUser()
            except Exception as e:
                print("JWT Auth failed:", e)
                scope["user"] = AnonymousUser()
                
        print("Authenticated user:", scope["user"], scope["user"].is_authenticated)

        return await self.app(scope, receive, send)
