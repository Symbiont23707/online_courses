from django.urls import path
from .consumers import LectureNotificationConsumer

websocket_urlpatterns = [
    path('ws/lecture_notifications/<uuid:uuid>/', LectureNotificationConsumer.as_asgi()),
]