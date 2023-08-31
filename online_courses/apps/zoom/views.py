import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import hashlib
import hmac

from rest_framework import views

from apps.zoom.models import Meeting
from config import settings


class ZoomAPIClient(views.APIView):

    @staticmethod
    @csrf_exempt
    def zoom_api_client(request):
        body = json.loads(request.body)
        plain_token = body['payload']['plainToken']
        hash_for_validate = hmac.new(settings.ZOOM_SECRET_TOKEN.encode(), plain_token.encode(),
                                     hashlib.sha256).hexdigest()

        response_data = {
            'plainToken': plain_token,
            'encryptedToken': hash_for_validate
        }

        return JsonResponse(response_data)

    @staticmethod
    def get_access_token():
        url = "https://zoom.us/oauth/token"
        data = {
            "grant_type": "account_credentials",
            "account_id": settings.ZOOM_ACCOUNT_ID
        }
        response = requests.post(url, data=data, auth=(settings.ZOOM_CLIENT_ID, settings.ZOOM_CLIENT_SECRET))

        access_token = response.json()["access_token"]
        return access_token

    @staticmethod
    def create_zoom_meeting(topic, start_time, lecture):
        url = "https://api.zoom.us/v2/users/me/meetings"

        headers = {
            "Authorization": f"Bearer {ZoomAPIClient.get_access_token()}",
            "Content-Type": "application/json"
        }

        data = {
            "topic": topic,
            "type": "2",
            "start_time": start_time,
            "duration": "140",
            "timezone": "Europe/Minsk",
            "settings": {
                "host_video": "true",
                "participant_video": "true",
                "join_before_host": "true"
            }
        }

        response = requests.post(url, json=data, headers=headers)
        meeting_data = response.json()
        Meeting.objects.create(uuid=meeting_data['uuid'], meeting_id=int(meeting_data['id']),
                               host_email=meeting_data['host_email'], duration=int(meeting_data['duration']),
                               topic=topic, lecture=lecture, participants_count=0)

        return meeting_data['join_url']
