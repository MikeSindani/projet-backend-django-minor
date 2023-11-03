"""
ASGI config for PROJET_DJANGO_MINOR project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from minor_asset.routing import ws_urlpatterns
#from two.routing import ws_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'examplechannels.settings')

application = ProtocolTypeRouter(
    {
        'http': get_asgi_application(),
        'websocket': AllowedHostsOriginValidator(AuthMiddlewareStack(URLRouter(ws_urlpatterns))),
    }
)

