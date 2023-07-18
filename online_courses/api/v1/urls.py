from django.urls import path, include

from api.v1 import auth
from apps.courses.views import CourseAPIView, CourseDetailAPIView
from apps.home_tasks.views import Home_taskAPIView, HomeTaskResultAPIView, Home_taskDetailAPIView, \
    HomeTaskResultDetailAPIView
from apps.lectures.views import LectureAPIView, LectureDetailAPIView, LectureByCourseAPIView
from apps.marks.views import MarkAPIView, MarkDetailAPIView, CommentAPIView, CommentDetailAPIView
from apps.users.views import RegisterView

app_name = 'v1'

urlpatterns = [
    path('auth/', include(auth.urlpatterns)),
    path('users/', include([
        path('register/', RegisterView.as_view())])),
    path('courses/', include([
        path('', CourseAPIView.as_view()),
        path('<uuid:uuid>/', CourseDetailAPIView.as_view()),
    ])),
    path('lectures/', include([
        path('', LectureAPIView.as_view()),
        path('<uuid:uuid>/', LectureDetailAPIView.as_view()),
        path('course/<uuid:uuid>/', LectureByCourseAPIView.as_view())
    ])),
    path('home_tasks/', include([
        path('', Home_taskAPIView.as_view()),
        path('<uuid:uuid>/', Home_taskDetailAPIView.as_view()),
        path('completed/', HomeTaskResultAPIView.as_view()),
        path('<uuid:uuid>/', HomeTaskResultDetailAPIView.as_view()),
    ])),
    path('marks/', include([
        path('', MarkAPIView.as_view()),
        path('<uuid:uuid>/', MarkDetailAPIView.as_view()),
        path('comments/', CommentAPIView.as_view()),
        path('comments/<uuid:uuid>/', CommentDetailAPIView.as_view()),
    ])),
]
