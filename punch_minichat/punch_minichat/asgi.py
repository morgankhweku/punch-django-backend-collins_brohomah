"""
ASGI config for punch_minichat project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "punch_minichat.settings")
django.setup()


from chat.routing import websocket_urlpatterns as chat_ws
from groupchat.routing import websocket_urlpatterns as group_ws


from groupchat.middleware.jwt_auth_middleware import JWTAuthMiddleware


django_asgi_app = get_asgi_application()


all_ws_patterns = chat_ws + group_ws


application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": JWTAuthMiddleware(
        URLRouter(all_ws_patterns)
    ),
})

