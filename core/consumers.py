from channels.generic.websocket import AsyncWebsocketConsumer
import json

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Accepter la connexion WebSocket
        await self.accept()

        # Ajouter l'utilisateur à un groupe de notifications
        user_id = self.scope['user'].id
        await self.channel_layer.group_add(f"user_{user_id}", self.channel_name)

    async def disconnect(self, close_code):
        # Retirer l'utilisateur du groupe de notifications
        user_id = self.scope['user'].id
        await self.channel_layer.group_discard(f"user_{user_id}", self.channel_name)

    async def receive(self, text_data):
        # Recevoir un message du client WebSocket
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(f"Message reçu : {message}")

    async def send_notification(self, event):
        # Envoyer une notification au client WebSocket
        message = event['message']
        await self.send(text_data=json.dumps({'message': message}))