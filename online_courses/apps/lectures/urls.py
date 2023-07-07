from django.urls import path, include
from rest_framework import routers

from apps.lectures.views import LectureViewSet

router = routers.SimpleRouter()
router.register(r'lecture', LectureViewSet)

urlpatterns = [
    path('', include(router.urls))
]