import json
from django.test import TestCase
from apps.courses.models import Course
from apps.lectures.models import Lecture
from apps.zoom.models import Meeting
from config import settings
from libs.types import ZoomUrls
from libs.zoom_configuration import ZoomEvents


class WebhookZoomTest(TestCase):

    def setUp(self):

        self.zoom_secret_token = settings.ZOOM_SECRET_TOKEN
        self.course = Course.objects.create(
            name="Python", specialty='Programming'
        )

        self.schedule_data = {
            "hour": 10,
            "minute": 36,
            "active": True,
            "interval": "day"
        }

        self.lecture = Lecture.objects.create(
            topic="OOP",
            course=self.course,
            presentation='media/pop_y1PlE5O.pdf',
            schedule=self.schedule_data
        )
        self.url = ZoomUrls.zoom_webhook_url

    def test_handle_meeting_participant_joined(self):

        meeting = Meeting.objects.create(
            meeting_id=79164111853,
            duration=140,
            lecture_id=self.lecture.uuid,
            participants_count=0
        )

        event_data = {
            "event": ZoomEvents.meeting_participant_joined,
            "payload": {
                "object": {
                    "id": 79164111853
                }
            }
        }
        response = self.client.post(self.url, data=json.dumps(event_data), content_type='application/json')
        updated_meeting = Meeting.objects.get(meeting_id=meeting.meeting_id)
        self.assertEqual(updated_meeting.participants_count, 1)


    def test_handle_endpoint_url_validation(self):

        event_data = {
            "event": ZoomEvents.endpoint_url_validation,
            "payload": {
                "plainToken": "dB0AKIijQui97J3R9poThA"
            }
        }

        response = self.client.post(self.url, data=json.dumps(event_data), content_type='application/json')
        payload = json.loads(response.content.decode())

        self.assertIn(payload['plainToken'], 'dB0AKIijQui97J3R9poThA')
        self.assertIn(payload['encryptedToken'], '1e408952ca871df783be09e591a1f1dad2ece5883b02ddd112ac77ac7d8fc3ae')