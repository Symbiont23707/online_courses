import json

from rest_framework import status
from rest_framework.test import APITestCase
from apps.courses.models import Course
from apps.home_tasks.models import HomeTask
from apps.lectures.models import Lecture
from apps.users.models import Teacher, User, Student
from libs.types import HomeTaskUrls


class HomeTasksAPIViewTest(APITestCase):
    def setUp(self):
        self.teacher = Teacher.objects.create(
            user=User.objects.create_user(
                username='teacher',
                password='password',
                email='teacher@teacher.com',
            )
        )
        self.student = Student.objects.create(
            user=User.objects.create_user(
                username='student',
                password='password',
                email='student@student.com',
            ),
            specialty='Programming'
        )
        self.course = Course.objects.create(
            name='Python',
            specialty='Programming'
        )
        self.course2 = Course.objects.create(
            name='Java',
            specialty='Programming'
        )
        self.course.teachers.add(self.teacher)
        self.course.students.add(self.student)
        self.course2.teachers.add(self.teacher)
        schedule_data = {
            "hour": 10,
            "minute": 36,
            "active": True,
            "interval": "day"
        }
        self.lecture2 = Lecture.objects.create(
            topic="POP",
            course=self.course2,
            presentation='media/pop_y1PlE5O.pdf',
            schedule=schedule_data
        )
        self.lecture = Lecture.objects.create(
            topic="OOP",
            course=self.course,
            presentation='media/pop_y1PlE5O.pdf',
            schedule=schedule_data
        )
        self.home_task = HomeTask.objects.create(
            description='OOP',
            lectures=self.lecture
        )
        self.url = HomeTaskUrls.home_task_api_view_url

    def test_list_home_tasks_from_teacher_success(self):
        self.client.login(username='teacher', password='password')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('OOP', json.loads(response.content.decode())['results'][0]['description'])

    def test_list_home_tasks_from_student_success(self):
        self.client.login(username='student', password='password')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('OOP', json.loads(response.content.decode())['results'][0]['description'])

    def test_create_home_tasks_success(self):
        self.client.login(username='teacher', password='password')
        data = {
            'description': 'POP',
            'lectures': self.lecture2.uuid
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_home_task = HomeTask.objects.get(description='POP')
        self.assertIsNotNone(created_home_task)

    def test_create_home_tasks_failure(self):
        self.client.login(username='student', password='password')
        data = {
            'description': 'POP',
            'lectures': self.lecture2.uuid
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)