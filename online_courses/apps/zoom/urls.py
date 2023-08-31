from django.urls import path
from apps.zoom.views import ZoomAPIClient

urlpatterns = [
    path('event_notification/', ZoomAPIClient.zoom_api_client),
]