from django.urls import path, include

from apps.courses.views import CourseAPIView, CourseDetailAPIView
from apps.home_tasks.views import HomeTaskAPIView, HomeTaskResultAPIView, HomeTaskDetailAPIView, \
    HomeTaskResultDetailAPIView
from apps.lectures.views import LectureAPIView, LectureDetailAPIView, LectureByCourseAPIView
from apps.marks.views import MarkAPIView, MarkDetailAPIView, CommentAPIView, CommentDetailAPIView
from apps.users.views import RegisterView

app_name = 'v1'

urlpatterns = [
    path('users/', include([
        path('register/', RegisterView.as_view())])),
    path('courses/', include([
        path('', CourseAPIView.as_view()),
        path('<uuid:uuid>/', CourseDetailAPIView.as_view()),
        path('<uuid:uuid>/lectures/', LectureByCourseAPIView.as_view())
    ])),
    path('lectures/', include([
        path('', LectureAPIView.as_view()),
        path('<uuid:uuid>/', LectureDetailAPIView.as_view())
    ])),
    path('home_tasks/', include([
        path('', HomeTaskAPIView.as_view()),
        path('<uuid:uuid>/', HomeTaskDetailAPIView.as_view()),
        path('completed/', HomeTaskResultAPIView.as_view()),
        path('completed/<uuid:uuid>/', HomeTaskResultDetailAPIView.as_view()),
    ])),
    path('marks/', include([
        path('', MarkAPIView.as_view()),
        path('<uuid:uuid>/', MarkDetailAPIView.as_view()),
        path('comments/', CommentAPIView.as_view()),
        path('comments/<uuid:uuid>/', CommentDetailAPIView.as_view()),
    ])),
]
