import json
from rest_framework import status
from rest_framework.test import APITestCase
from apps.courses.models import Course
from apps.home_tasks.models import HomeTask, HomeTaskResult
from apps.lectures.models import Lecture
from apps.users.models import Teacher, User, Student
from libs.types import HomeTaskUrls, HomeTaskResultUrls


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
        self.home_task1 = HomeTask.objects.create(
            description='OOP',
            lectures=self.lecture
        )
        self.home_task_result = HomeTaskResult.objects.create(
            answer='is a computer programming model that organizes software design around data, or objects, '
                   'rather than functions and logic.',
            home_task=self.home_task1,
            student=self.student
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


class HomeTasksDetailAPIViewTest(APITestCase):
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
        self.home_task1 = HomeTask.objects.create(
            description='OOP',
            lectures=self.lecture
        )
        self.home_task2 = HomeTask.objects.create(
            description='POP',
            lectures=self.lecture2
        )
        self.url = HomeTaskUrls.home_task_api_view_url

    def test_home_task_retrieve_teacher_success(self):
        self.client.login(username='teacher', password='password')
        response = self.client.get(f'{self.url}{self.home_task1.uuid}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_home_task_retrieve_student_success(self):
        self.client.login(username='student', password='password')
        response = self.client.get(f'{self.url}{self.home_task1.uuid}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_home_task_retrieve_teacher_failure(self):
        self.client.login(username='teacher', password='password')
        response = self.client.get(f'{self.url}{self.home_task2.uuid}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_home_task_retrieve_student_failure(self):
        self.client.login(username='student', password='password')
        response = self.client.get(f'{self.url}{self.home_task2.uuid}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_home_task_teacher_success(self):
        self.client.login(username='teacher', password='password')
        updated_data = {
            'description': 'Introduction OOP',
            'lectures': self.lecture,
        }
        response = self.client.put(f'{self.url}{self.home_task1.uuid}/', updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], 'Introduction OOP')

    def test_update_home_task_student_failure(self):
        self.client.login(username='student', password='password')
        updated_data = {
            'description': 'Introduction OOP',
            'lectures': self.lecture,
        }
        response = self.client.put(f'{self.url}{self.home_task1.uuid}/', updated_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_home_task_delete_teacher_success(self):
        self.client.login(username='teacher', password='password')
        response = self.client.delete(f'{self.url}{self.home_task1.uuid}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_home_task_delete_student_failure(self):
        self.client.login(username='student', password='password')
        response = self.client.delete(f'{self.url}{self.home_task1.uuid}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class HomeTasksResultAPIViewTest(APITestCase):
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
        self.home_task_result = HomeTaskResult.objects.create(
            answer='is a computer programming model that organizes software design around data, or objects, '
                   'rather than functions and logic.',
            home_task=self.home_task,
            student=self.student
        )
        self.url = HomeTaskResultUrls.home_task_result_api_view_url

    def test_list_home_tasks_result_from_teacher_success(self):
        self.client.login(username='teacher', password='password')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_home_tasks_result_from_student_success(self):
        self.client.login(username='student', password='password')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_home_tasks_result_student_failure(self):
        self.client.login(username='student', password='password')
        data = {
            'answer': 'is a computer programming model that organizes software design around data, or objects, '
                   'rather than functions and logic.',
            'home_task': self.home_task.uuid,
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_home_tasks_result_teacher_success(self):
        self.client.login(username='teacher', password='password')
        data = {
            'answer': 'is a computer programming model that organizes software design around data, or objects, '
                   'rather than functions and logic.',
            'home_task': self.home_task.uuid,
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class HomeTasksResultDetailAPIViewTest(APITestCase):
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
        self.home_task1 = HomeTask.objects.create(
            description='OOP',
            lectures=self.lecture
        )
        self.home_task2 = HomeTask.objects.create(
            description='POP',
            lectures=self.lecture2
        )

        self.home_task_result1 = HomeTaskResult.objects.create(
            answer='is a computer programming model that organizes software design around data, or objects, '
                   'rather than functions and logic.',
            home_task=self.home_task1,
            student=self.student
        )
        self.home_task_result2 = HomeTaskResult.objects.create(
            answer='refers to Procedural Oriented Programming and deals with programs and functions. '
                   'Programs are divided into functions and data is global',
            home_task=self.home_task2,
            student=self.student
        )
        self.url = HomeTaskResultUrls.home_task_result_api_view_url

    def test_home_task_result_retrieve_teacher_success(self):
        self.client.login(username='teacher', password='password')
        response = self.client.get(f'{self.url}{self.home_task_result1.uuid}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_home_task_result_retrieve_student_success(self):
        self.client.login(username='student', password='password')
        response = self.client.get(f'{self.url}{self.home_task_result1.uuid}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_home_task_retrieve_teacher_failure(self):
        self.client.login(username='teacher', password='password')
        response = self.client.get(f'{self.url}{self.home_task2.uuid}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_home_task_retrieve_student_failure(self):
        self.client.login(username='student', password='password')
        response = self.client.get(f'{self.url}{self.home_task2.uuid}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_home_task_result_student_success(self):
        self.client.login(username='student', password='password')
        updated_data = {
            'answer': 'is a computer programming model that organizes software design around data or objects.',
            'home_task': self.home_task1,
            'student': self.student
        }
        response = self.client.put(f'{self.url}{self.home_task_result1.uuid}/', updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['answer'],
            'is a computer programming model that organizes software design around data or objects.')

    def test_update_home_task_result_teacher_failure(self):
        self.client.login(username='teacher', password='password')
        updated_data = {
            'answer': 'refers to Procedural Oriented Programming.',
            'home_task': self.home_task1,
            'student': self.student
        }
        response = self.client.put(f'{self.url}{self.home_task_result1.uuid}/', updated_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_home_task_result_delete_student_success(self):
        self.client.login(username='student', password='password')
        response = self.client.delete(f'{self.url}{self.home_task_result1.uuid}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_home_task_result_delete_teacher_failure(self):
        self.client.login(username='teacher', password='password')
        response = self.client.delete(f'{self.url}{self.home_task_result1.uuid}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)