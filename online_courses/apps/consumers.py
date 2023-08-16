from channels.exceptions import DenyConnection
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.core.mail import send_mail
from config import settings


class LectureNotificationConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        if not self.scope['user'].is_authenticated:
            raise DenyConnection('Invalid User')
        group_name = self.get_lecture_uuid()

        await self.channel_layer.group_add(
            group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        group_name = self.get_lecture_uuid()
        await self.channel_layer.group_discard(group_name, self.channel_name)

    async def receive(self, text_data):
        pass

    async def lecture_notification(self, event):
        send_mail(event.get('subject'), event.get('message'), settings.EMAIL_HOST_USER, event.get('recipient_list'),
                  fail_silently=False)
        await self.send_json(event)

    def get_lecture_uuid(self):
        lecture_uuid = self.scope['url_route']['kwargs']['uuid']
        return f'lecture_notifications_{lecture_uuid}'
