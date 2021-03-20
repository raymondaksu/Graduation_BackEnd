from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import chat.routing
import os

import django
django.setup()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog_project.settings")

# django_application = get_asgi_application()

# async def application(scope, receive, send):
#     if scope['type'] == 'http':
#         # Let Django handle HTTP requests
#         await django_application(scope, receive, send)
#     elif scope['type'] == 'websocket':
#         # We'll handle Websocket connections here
#         await AuthMiddlewareStack(
#             URLRouter(
#                 chat.routing.websocket_urlpatterns
#             )
#         )
#     else:
#         raise NotImplementedError(f"Unknown scope type {scope['type']}")

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    )
})
