"""
ASGI config for esafety project.
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'esafety.settings')

django_asgi_app = get_asgi_application()

# WebSocket routing (to be configured later)
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter([
            # WebSocket routes will be added here
        ])
    ),
})

