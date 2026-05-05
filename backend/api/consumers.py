import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User


class ChatConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for real-time chat in study rooms."""

    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'room_{self.room_id}'

        # Join the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        # Notify group that a user connected
        user = self.scope.get('user')
        if user and user.is_authenticated:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_join',
                    'username': user.username,
                    'user_id': user.id,
                }
            )

    async def disconnect(self, close_code):
        user = self.scope.get('user')
        if user and user.is_authenticated:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_leave',
                    'username': user.username,
                    'user_id': user.id,
                }
            )

        # Leave the room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """Handle incoming message from WebSocket client."""
        data = json.loads(text_data)
        msg_type = data.get('type', 'chat_message')
        user = self.scope.get('user')

        username = user.username if user and user.is_authenticated else 'Anonymous'
        user_id = user.id if user and user.is_authenticated else None

        if msg_type == 'chat_message':
            message = data.get('message', '')
            if not message.strip():
                return

            # Save message to database
            msg = await self.save_message(user_id, message)

            # Broadcast to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': username,
                    'user_id': user_id,
                    'message_id': msg.id if msg else None,
                    'is_ai': False,
                    'timestamp': msg.created_at.isoformat() if msg else None,
                }
            )
        elif msg_type in ['webrtc_offer', 'webrtc_answer', 'webrtc_ice_candidate']:
            # Relay WebRTC signaling data
            target_user_id = data.get('target_user_id')
            payload = data.get('payload')
            
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'webrtc_signal',
                    'signal_type': msg_type,
                    'sender_id': user_id,
                    'target_user_id': target_user_id,
                    'payload': payload,
                }
            )

    async def webrtc_signal(self, event):
        """Send WebRTC signal to target client."""
        user = self.scope.get('user')
        user_id = user.id if user and user.is_authenticated else None
        
        # Only send to the target user (or broadcast if no target)
        if not event.get('target_user_id') or event.get('target_user_id') == user_id:
            # Don't send back to the sender
            if event.get('sender_id') != user_id:
                await self.send(text_data=json.dumps({
                    'type': event['signal_type'],
                    'sender_id': event['sender_id'],
                    'payload': event['payload'],
                }))



    async def chat_message(self, event):
        """Send chat message to WebSocket client."""
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': event['message'],
            'username': event['username'],
            'user_id': event.get('user_id'),
            'message_id': event.get('message_id'),
            'is_ai': event.get('is_ai', False),
            'timestamp': event.get('timestamp'),
        }))

    async def user_join(self, event):
        """Notify client that a user joined."""
        await self.send(text_data=json.dumps({
            'type': 'user_join',
            'username': event['username'],
            'user_id': event['user_id'],
        }))

    async def user_leave(self, event):
        """Notify client that a user left."""
        await self.send(text_data=json.dumps({
            'type': 'user_leave',
            'username': event['username'],
            'user_id': event['user_id'],
        }))

    @database_sync_to_async
    def save_message(self, user_id, content):
        """Save a chat message to the database."""
        from .models import ChatMessage, StudyRoom
        try:
            room = StudyRoom.objects.get(id=self.room_id)
            user = User.objects.get(id=user_id) if user_id else None
            return ChatMessage.objects.create(
                room=room, user=user, content=content, is_ai=False
            )
        except (StudyRoom.DoesNotExist, User.DoesNotExist):
            return None
