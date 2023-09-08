from django.contrib.auth.views import PasswordResetView
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from apps.zoom.views import ZoomWebhookView

urlpatterns = [
    path('event_notification/', csrf_exempt(ZoomWebhookView.as_view())),
]