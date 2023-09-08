import hashlib
import hmac
import json
from django.db import transaction
from apps.zoom.models import Meeting
from libs.zoom_configuration import ZoomEvents


class WebhookZoom:

    def __init__(self, zoom_secret_token):
        self.zoom_secret_token = zoom_secret_token

    def handle_webhook_event(self, request):
        body = json.loads(request.body)
        event_handlers_map = {
            ZoomEvents.meeting_participant_joined: self.handle_meeting_participant_joined,
            ZoomEvents.endpoint_url_validation: self.handle_endpoint_url_validation,
        }
        event_type = body.get('event')
        if event_type in event_handlers_map:
            return event_handlers_map[event_type](body)

    @staticmethod
    @transaction.atomic
    def handle_meeting_participant_joined(body):
        meeting_id = body['payload']['object']['id']
        meeting = Meeting.objects.select_for_update().get(meeting_id=meeting_id)
        meeting.participants_count += 1
        meeting.save()

    def handle_endpoint_url_validation(self, body):
        plain_token = body['payload']['plainToken']
        hash_for_validate = hmac.new(self.zoom_secret_token.encode(), plain_token.encode(),
                                     hashlib.sha256).hexdigest()
        response_data = {
            'plainToken': plain_token,
            'encryptedToken': hash_for_validate
        }
        return response_data
