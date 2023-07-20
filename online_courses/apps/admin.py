from django.contrib import admin

from apps.courses.models import Course
from apps.home_tasks.models import HomeTaskResult, HomeTask
from apps.lectures.models import Lecture
from apps.marks.models import Mark, Comment
from apps.users.models import User, Teacher, Student

admin.site.register(User)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Lecture)
admin.site.register(HomeTask)
admin.site.register(HomeTaskResult)
admin.site.register(Mark)
admin.site.register(Comment)
