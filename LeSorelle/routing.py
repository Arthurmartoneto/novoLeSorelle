from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from channels.auth import AuthMiddlewareStack
from LeSorelle.consumers import NotificacaoConsumer
from django.urls import path
from .consumers import NotificacaoConsumer

websocket_urlpatterns = [
    path('ws/notificacoes/', NotificacaoConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter([
            path('ws/notificacoes/', NotificacaoConsumer.as_asgi()),
        ])
    ),
})