from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter

from .views import CourseViewSet, AddTeacher, AddDeleteStudent

router = routers.SimpleRouter()
router.register(r'course', CourseViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('add_teacher/', AddTeacher.as_view()),
    path('students/', AddDeleteStudent.as_view())
]
