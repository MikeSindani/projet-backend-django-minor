from django.urls import path
from minor_asset.consumers import OneConsumer

ws_urlpatterns = [
    path('ws/one/', OneConsumer.as_asgi())
]