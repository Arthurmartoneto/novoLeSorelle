from channels.generic.websocket import AsyncWebsocketConsumer
import json

class NotificacaoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Join room group
        await self.channel_layer.group_add("notificacoes_operador", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard("notificacoes_operador", self.channel_name)

    # Receive message from room group
    async def enviar_notificacao(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))