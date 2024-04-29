"""
ASGI config for chatbot project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chatbot.settings")

application = get_asgi_application()

import core.routing

application = ProtocolTypeRouter({
    "http": application,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(URLRouter(core.routing.websocket_urlpatterns))
    ),
})
