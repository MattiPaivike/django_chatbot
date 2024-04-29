from django.urls import path, re_path
from . import consumers


websocket_urlpatterns = [
    re_path(r'ws/ai-demo/(?P<conversation_id>[0-9a-fA-F-]+)/$', consumers.ChatConsumer.as_asgi(), name="ws_ai_demo_new_chat"),
]
