import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Try to get the room name from the URL route kwargs (normal case).
        # If it's missing (some routing misconfiguration), fall back to parsing
        # the path (e.g. /ws/chat/<room>/) to avoid KeyError and reject
        # gracefully if we still can't determine a room.
        url_route = self.scope.get("url_route") or {}
        kwargs = url_route.get("kwargs") or {}
        room = kwargs.get("room")
        if not room:
            # Fallback: try to parse from scope['path']
            path = self.scope.get("path", "")
            # Expecting something like /ws/chat/<room>/
            parts = [p for p in path.split("/") if p]
            try:
                # parts = ['ws', 'chat', '<room>']
                room = parts[2]
            except Exception:
                # Could not determine room: reject the connection
                await self.close()
                return

        self.room = room
        self.group_name = f"chat_{self.room}"

        # Use the group_name when adding to channel layer groups.
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chat.message",
                "message": f"[SYSTEM] joined room: {self.room}",
            }
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        msg = data["message"]

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chat.message",
                "message": msg,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"]
        }))