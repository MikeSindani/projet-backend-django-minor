from django.urls import path,re_path
from . import consumers

ws_dash_urlpatterns = [
    path('ws/asset/one/', consumers.OneConsumer.as_asgi()),
    re_path(r'^ws/Notification/(?P<organization_id>[^/]+)/$', consumers.NotificationConsumer.as_asgi()),
    path('ws/Content/', consumers.ContentConsumer.as_asgi()),
]