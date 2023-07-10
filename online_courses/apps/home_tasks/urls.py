from django.urls import path

from .views import HomeTask, Completed_Home_task, MyHomeTasks

urlpatterns = [
    path('home_task/', HomeTask.as_view()),
    path('completed_home_task/', Completed_Home_task.as_view()),
    path('my_home_tasks/', MyHomeTasks.as_view())
]