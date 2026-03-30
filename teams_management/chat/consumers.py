import json
from django.utils import timezone
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from teams_management.user_profiles.models import UserProfile
from rest_framework.authtoken.models import Token
from .models import Message, Room

class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        
        query_string = self.scope.get("query_string", b"").decode()
        query_params = dict(qp.split("=") for qp in query_string.split("&") if "=" in qp)
        token_key = query_params.get("token")


        if token_key:
            user = await self.get_user_from_token(token_key)
            if user:
                self.scope['user'] = user

        if not self.scope['user'].is_authenticated:
            print(f"REJECTED: {self.scope['user']} attempted to connect.")
            await self.close()
            return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        print(f"CONNECTED: {self.scope['user'].username} in {self.room_name}")
        
        all_users = await self.get_all_system_users()
        history = await self.get_room_history()

        await self.send(text_data=json.dumps({
            'type': 'initial_data',
            'all_users': all_users,
            'users': history
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type')

        display_name = await self.get_display_name()    

        if message_type == 'chat_message':
            message = data['message']

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': display_name,
                    'timestamp': str(timezone.now())
                }
            )
        elif message_type == 'typing':
            username = self.scope['user'].get_username()    

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
        room, _ = Room.objects.get_or_create(slug= self.room_name)
        user_profile = UserProfile.objects.get(user_id= self.scope['user'].id)
       
        return Message.objects.create(
            room= room,
            user = user_profile,
            content = message
        )
    @database_sync_to_async
    def get_all_system_users(self):
        users = UserProfile.objects.all()
        return [
            {
                "id": u.user.id,
                "display_name": getattr(u, 'display_name', u.display_name),
            } for u in users
        ]

    @database_sync_to_async
    def get_room_history(self):
        room, _ = Room.objects.get_or_create(slug= self.room_name)
        messages = room.messages.select_related('user').order_by('-created_at')[:50]
        return [
            {
                "message": m.content,
                "username": m.user.display_name,
                "timestamp": str(m.created_at)
            } for m in messages
        ]
    
    @database_sync_to_async
    def get_display_name(self):
        user = self.scope['user']

        if user.is_authenticated:

            if hasattr(user, 'profile'):
                return user.profile.display_name
            return user.get_username
        return "Guest"
    
    @database_sync_to_async
    def get_user_from_token(self, key):
        try: 
            return Token.objects.get(key=key).user
        
        except Exception:
            return None