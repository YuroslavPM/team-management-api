import json
from django.utils import timezone
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from teams_management.user_profiles.models import UserProfile
from .models import Message, Room

class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        users = await self.get_room_users()
        await self.send(text_data=json.dumps({
            'type': 'user_list',
            'users': users
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type')

        if message_type == 'chat_message':
            message = data['message']
            username = self.scope['user'].get_username

            await self.save_message(message)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': username,
                    'timestamp': str(timezone.now())
                }
            )
        elif message_type == 'typing':
            username = self.scope['user'].get_username    

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_typing',
                    'username': username
                }
            )

    async def chat_message(self, event):

        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': event['message'],
            'username': event['username'],
            'timestamp': event['timestamp'],
        }))


    async def user_typing(self, event):
        await self.send(text_data=json.dumps({
            'type': 'typing',
            'username': event['username']
        }))


    @database_sync_to_async
    def save_message(self, message):
        room = Room.objects.get_or_create(slug= self.room_name)
        return Message.objects.create(
            room= room,
            user = self.scope['user'],
            content = message
        )
    
    @database_sync_to_async
    def get_room_users(self):
        room, created = Room.objects.get_or_create(slug= self.room_name)
        messages = room.messages.select_related('user').order_by('-created_at')[:50]
        users = set(msg.user.username for msg in messages)
        return list(users)