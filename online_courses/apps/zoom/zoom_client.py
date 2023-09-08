import requests
from libs.zoom_configuration import ZoomUrls


class ZoomAPIClient:
    def __init__(self, zoom_secret_token, zoom_account_id, zoom_client_id, zoom_client_secret):
        self.zoom_secret_token = zoom_secret_token
        self.zoom_account_id = zoom_account_id
        self.zoom_client_id = zoom_client_id
        self.zoom_client_secret = zoom_client_secret
        self.access_token = self.get_access_token('account_credentials')

    def _get_headers(self, content_type):
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": content_type
        }

    def get_access_token(self, grant_type):
        url = ZoomUrls.token
        data = {
            "grant_type": grant_type,
            "account_id": self.zoom_account_id
        }
        response = requests.post(url, data=data, auth=(self.zoom_client_id, self.zoom_client_secret))
        access_token = response.json()["access_token"]
        return access_token

    def create_zoom_meeting(self, topic, start_time, content_type, data):
        url = ZoomUrls.zoom_meeting
        headers = self._get_headers(content_type)
        data['topic'] = topic
        data['start_time'] = start_time
        response = requests.post(url, json=data, headers=headers)
        meeting_data = response.json()
        return meeting_data
