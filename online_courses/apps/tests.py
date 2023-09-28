from django.test import TestCase
from unittest.mock import patch
from apps.courses.models import Course
from apps.lectures.models import Lecture
from apps.tasks import send_lecture_notifications
from apps.zoom.models import Meeting
import arrow


class SendLectureNotificationsTest(TestCase):

    @patch('apps.zoom.zoom_client.ZoomAPIClient.create_zoom_meeting')
    def test_send_lecture_notifications(self, mock_create_zoom_meeting):
        now = arrow.utcnow()
        course = Course.objects.create(
            name="Python", specialty='Programming'
        )

        schedule_data = {
            "hour": 10,
            "minute": 36,
            "active": True,
            "interval": "day"
        }

        lecture = Lecture.objects.create(
            topic="OOP",
            course=course,
            presentation='media/pop_y1PlE5O.pdf',
            schedule=schedule_data
        )

        meeting = Meeting.objects.create(
            uuid='YuuiTnIvTS+z59BfSwCazw==',
            meeting_id=75318246179,
            topic='OOP',
            lecture_id=lecture.uuid,
            duration=140,
            host_email='yauheni.bykau@leverx.com'
        )

        mock_create_zoom_meeting.return_value = {
            'uuid': 'YuuiTnIvTS+z59BfSwCazw==',
            'id': '75318246179',
            'host_email': 'yauheni.bykau@leverx.com',
            'topic': 'OOP',
            'duration': 140,
            'join_url': 'https://zoom.us/join/75318246179'
        }

        send_lecture_notifications()
        meeting.refresh_from_db()

        self.assertEqual(meeting.uuid, 'YuuiTnIvTS+z59BfSwCazw==')
        self.assertEqual(meeting.meeting_id, 75318246179)
        self.assertEqual(meeting.host_email, 'yauheni.bykau@leverx.com')
        self.assertEqual(meeting.duration, 140)
        self.assertEqual(meeting.topic, 'OOP')

