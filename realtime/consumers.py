from channels.generic.websocket import AsyncJsonWebsocketConsumer


class NotificationConsumer(AsyncJsonWebsocketConsumer):
    """Websocket endpoint for real-time notifications.

    Authenticated users connect to ws/notifications/ and join the group
    ``user_<pk>``. The notification helper (realtime.utils.notify_user)
    publishes to that group so connected clients receive new notifications
    as they are created.
    """

    async def connect(self):
        self.user = self.scope.get('user')
        if self.user is None or self.user.is_anonymous:
            await self.close(code=4001)
            return
        self.group_name = 'user_%s' % self.user.pk
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        group_name = getattr(self, 'group_name', None)
        if group_name is not None:
            await self.channel_layer.group_discard(group_name, self.channel_name)

    async def receive_json(self, content, **kwargs):
        if isinstance(content, dict) and content.get('action') == 'ping':
            await self.send_json({'action': 'pong'})

    async def notification_message(self, event):
        """Group message handler: relays a notification payload to the client."""
        await self.send_json(event['message'])