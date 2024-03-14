from django.urls import path
from .consumer import *

websocket_urlpatterns = [
    path('ws/sc/', CustSyncConsumer.as_asgi()),
    # path('ws/ac/', CustAsyncConsumer.as_asgi()),
]
