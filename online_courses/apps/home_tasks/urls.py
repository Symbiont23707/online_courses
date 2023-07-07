from django.urls import path

from .views import HomeTask, Completed_Home_task

urlpatterns = [
    path('home_task/', HomeTask.as_view()),
    path('completed_home_task/', Completed_Home_task.as_view()),
]