import json

from channels.db import database_sync_to_async
from channels.exceptions import DenyConnection
from channels.generic.websocket import AsyncWebsocketConsumer, AsyncJsonWebsocketConsumer
from asgiref.sync import async_to_sync, sync_to_async
import arrow
from django.core.mail import send_mail
from django.db.models import Q

from apps.lectures.models import Lecture
from config import settings
from libs.types import StatusLecture, Intervals, MessageEmail


class LectureNotificationConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        # if not self.scope['user'].is_authenticated:
        #     raise DenyConnection('Invalid User')
        lecture_uuid = self.scope['url_route']['kwargs']['uuid']
        group_name = f'lecture_notifications_{lecture_uuid}'

        await self.channel_layer.group_add(
            group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # course_uuid = self.scope['url_route']['kwargs']['course_uuid']
        # group_name = f'lecture_notifications_{course_uuid}'
        # await self.channel_layer.group_discard(group_name, self.channel_name)
        pass

    async def receive(self, text_data):
        pass

    async def lecture_notification(self, event):
        send_mail(event.get('subject'), event.get('message'), settings.EMAIL_HOST_USER, event.get('recipient_list'),
                  fail_silently=False)
        await self.send_json(event)
