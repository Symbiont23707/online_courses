from rest_framework import status
from rest_framework.test import APITestCase
from apps.courses.models import Course
from apps.home_tasks.models import HomeTask, HomeTaskResult
from apps.lectures.models import Lecture
from apps.marks.models import Mark, Comment
from apps.users.models import Teacher, User, Student
from libs.types import MarkUrls, CommentUrls


class MarkAPIViewTest(APITestCase):
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
        self.mark1 = Mark.objects.create(
            rating='done',
            home_task_result=self.home_task_result1,
            created_by=self.teacher.user
        )
        self.url = MarkUrls.mark_api_view_url

    def test_list_marks_teacher_success(self):
        self.client.login(username='teacher', password='password')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_marks_student_success(self):
        self.client.login(username='student', password='password')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_mark_teacher_success(self):
        self.client.login(username='teacher', password='password')
        data = {
            'rating': 'overdue',
            'home_task_result': self.home_task_result2,
            'created_by': self.teacher.user
        }
        response = self.client.post(self.url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_mark_student_failure(self):
        self.client.login(username='student', password='password')
        data = {
            'rating': 'overdue',
            'home_task_result': self.home_task_result2,
            'created_by': self.teacher.user
        }
        response = self.client.post(self.url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class MarkDetailAPIViewTest(APITestCase):
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
        self.mark1 = Mark.objects.create(
            rating='done',
            home_task_result=self.home_task_result1,
            created_by=self.teacher.user
        )
        self.mark2 = Mark.objects.create(
            rating='overdue',
            home_task_result=self.home_task_result2,
            created_by=self.teacher.user
        )
        self.url = MarkUrls.mark_api_view_url

    def test_mark_retrieve_teacher_success(self):
        self.client.login(username='teacher', password='password')
        response = self.client.get(f'{self.url}{self.mark1.uuid}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_mark_retrieve_student_success(self):
        self.client.login(username='student', password='password')
        response = self.client.get(f'{self.url}{self.mark1.uuid}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_mark_retrieve_teacher_failure(self):
        self.client.login(username='teacher', password='password')
        response = self.client.get(f'{self.url}{self.mark2.uuid}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_mark_teacher_success(self):
        self.client.login(username='teacher', password='password')
        updated_data = {
            'rating': 'overdue',
            'home_task_result': self.home_task_result1,
            'created_by': self.teacher.user
        }
        response = self.client.put(f'{self.url}{self.mark1.uuid}/', updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['rating'], 'overdue')

    def test_update_home_task_student_failure(self):
        self.client.login(username='student', password='password')
        updated_data = {
            'rating': 'overdue',
            'home_task_result': self.home_task_result1,
            'created_by': self.teacher.user
        }
        response = self.client.put(f'{self.url}{self.mark1.uuid}/', updated_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_home_task_delete_teacher_success(self):
        self.client.login(username='teacher', password='password')
        response = self.client.delete(f'{self.url}{self.mark1.uuid}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_home_task_delete_student_failure(self):
        self.client.login(username='student', password='password')
        response = self.client.delete(f'{self.url}{self.mark1.uuid}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CommentAPIViewTest(APITestCase):
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
        self.mark1 = Mark.objects.create(
            rating='done',
            home_task_result=self.home_task_result1,
            created_by=self.teacher.user
        )
        self.mark2 = Mark.objects.create(
            rating='overdue',
            home_task_result=self.home_task_result2,
            created_by=self.teacher.user
        )
        self.comment1 = Comment.objects.create(
            mark= self.mark1,
            comment='U can do it better',
            created_by=self.teacher.user
        )
        self.url = CommentUrls.comment_api_view_url

    def test_list_comments_teacher_success(self):
        self.client.login(username='teacher', password='password')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_comments_student_success(self):
        self.client.login(username='student', password='password')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_comment_teacher_success(self):
        self.client.login(username='teacher', password='password')
        data = {
            'mark': self.mark2,
            'comment': 'U can do it better',
            'created_by': self.teacher.user
        }
        response = self.client.post(self.url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class CommentDetailAPIViewTest(APITestCase):
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
        self.mark1 = Mark.objects.create(
            rating='done',
            home_task_result=self.home_task_result1,
            created_by=self.teacher.user
        )
        self.mark2 = Mark.objects.create(
            rating='overdue',
            home_task_result=self.home_task_result2,
            created_by=self.teacher.user
        )
        self.comment1 = Comment.objects.create(
            mark= self.mark1,
            comment='U can do it better',
            created_by=self.teacher.user
        )
        self.url = CommentUrls.comment_api_view_url

    def test_comment_retrieve_teacher_success(self):
        self.client.login(username='teacher', password='password')
        response = self.client.get(f'{self.url}{self.comment1.uuid}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_comment_retrieve_student_success(self):
        self.client.login(username='student', password='password')
        response = self.client.get(f'{self.url}{self.comment1.uuid}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_comment_retrieve_teacher_failure(self):
        self.client.login(username='teacher', password='password')
        response = self.client.get(f'{self.url}{self.mark2.uuid}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_mark_teacher_success(self):
        self.client.login(username='teacher', password='password')
        updated_data = {
            'mark': self.mark1,
            'comment': 'Good job',
            'created_by': self.teacher.user
        }
        response = self.client.put(f'{self.url}{self.comment1.uuid}/', updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['comment'], 'Good job')

    def test_update_home_task_student_failure(self):
        self.client.login(username='student', password='password')
        updated_data = {
            'mark': self.mark1,
            'comment': 'Good job',
            'created_by': self.teacher.user
        }
        response = self.client.put(f'{self.url}{self.comment1.uuid}/', updated_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_home_task_delete_teacher_success(self):
        self.client.login(username='teacher', password='password')
        response = self.client.delete(f'{self.url}{self.comment1.uuid}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_home_task_delete_student_failure(self):
        self.client.login(username='student', password='password')
        response = self.client.delete(f'{self.url}{self.comment1.uuid}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)