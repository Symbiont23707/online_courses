from django.http import JsonResponse
from django.views import View
from apps.zoom.webhook_zoom import WebhookZoom
from config import settings


class ZoomWebhookView(View):
    zoom_secret_token = settings.ZOOM_SECRET_TOKEN

    def post(self, request):
        webhook = WebhookZoom(self.zoom_secret_token)
        response_data = webhook.handle_webhook_event(request)
        return JsonResponse(response_data)
