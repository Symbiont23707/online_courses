from django.db import models


class ZoomUrls(models.TextChoices):
    token = 'https://zoom.us/oauth/token'
    zoom_meeting = 'https://api.zoom.us/v2/users/me/meetings'


data = {
    "topic": 'Topic',
    "type": "2",
    "start_time": 'Time',
    "duration": "140",
    "timezone": "Europe/Minsk",
    "settings": {
        "host_video": "true",
        "participant_video": "true",
        "join_before_host": "true"
    }
}


class ZoomStatus(models.TextChoices):
    increment_status = 'Increased the number of participants by 1 in '


class ZoomEvents(models.TextChoices):
    meeting_participant_joined = 'meeting.participant_joined'
    endpoint_url_validation = 'endpoint.url_validation'
    event_not_exist = 'not exist in event_handlers_map'
