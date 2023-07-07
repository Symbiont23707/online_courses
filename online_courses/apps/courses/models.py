from django.db import models

from apps.teachers.models import Teacher
from apps.students.models import Student
from apps.users.models import BaseUUIDModel


# Create your models here.


class Course(BaseUUIDModel):
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)
    # related name
    teachers = models.ManyToManyField(Teacher, through='IntermediateCourseTeacher')
    students = models.ManyToManyField(Student, through='IntermediateCourseStudent')

    def __str__(self):
        return self.name


class IntermediateCourseTeacher(BaseUUIDModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)


class IntermediateCourseStudent(BaseUUIDModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
