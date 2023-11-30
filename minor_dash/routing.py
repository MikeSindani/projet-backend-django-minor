from django.urls import path,re_path
from . import consumers

ws_dash_urlpatterns = [
    path('ws/asset/one/', consumers.OneConsumer.as_asgi()),
    path('ws/Notification/', consumers.NotificationConsumer.as_asgi()),
    path('ws/Content/', consumers.ContentConsumer.as_asgi()),
]