from django.urls import path, include
from rest_framework import routers

from apps.marks.views import MarkViewSet, Comments

router = routers.SimpleRouter()
router.register(r'mark', MarkViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('comments/', Comments.as_view())
    ]