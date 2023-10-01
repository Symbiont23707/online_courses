from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase
from apps.courses.models import Course
from apps.lectures.models import Lecture
from apps.users.models import Teacher, Student, User
from libs.types import LectureUrls


class LectureAPIViewTest(APITestCase):
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
        self.schedule_data = {
            'weekday': None,
            'day': None,
            'hour': 10,
            'minute': 36,
            'active':'active',
            'interval': "day"
        }
        self.lecture = Lecture.objects.create(
            topic="OOP",
            course=self.course,
            presentation='media/pop_y1PlE5O.pdf',
            schedule=self.schedule_data
        )
        self.lecture2 = Lecture.objects.create(
            topic="POP",
            course=self.course2,
            presentation='media/pop_y1PlE5O.pdf',
            schedule=self.schedule_data
        )
        self.url = LectureUrls.lecture_api_view_url

    def test_list_lectures_teacher_success(self):
        self.client.login(username='teacher', password='password')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_lectures_student_success(self):
        self.client.login(username='student', password='password')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_lecture_teacher_success(self):
        self.client.login(username='teacher', password='password')
        presentation_file = SimpleUploadedFile(
            "pop_y1PlE5O.pdf",
            b"file_content",
            content_type="application/pdf"
        )
        data = {
            'topic': 'Advanced Python',
            'course': str(self.course2.uuid),
            'presentation': presentation_file,
            'schedule.weekday': '',
            'schedule.day': '',
            'schedule.hour': 10,
            'schedule.minute': 36,
            'schedule.active': 'active',
            'schedule.interval': 'day',
        }
        response = self.client.post(self.url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_lecture_student_failure(self):
        self.client.login(username='student', password='password')
        presentation_file = SimpleUploadedFile(
            "pop_y1PlE5O.pdf",
            b"file_content",
            content_type="application/pdf"
        )
        data = {
            'topic': 'Advanced Python',
            'course': str(self.course2.uuid),
            'presentation': presentation_file,
            'schedule.weekday': '',
            'schedule.day': '',
            'schedule.hour': 10,
            'schedule.minute': 36,
            'schedule.active': 'active',
            'schedule.interval': 'day',
        }
        response = self.client.post(self.url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class LectureDetailAPIViewTest(APITestCase):
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
        self.course1 = Course.objects.create(
            name='Python',
            specialty='Programming'
        )
        self.course2 = Course.objects.create(
            name='Java',
            specialty='Programming'
        )
        self.course1.teachers.add(self.teacher)
        self.course1.students.add(self.student)
        self.course2.students.add(self.student)
        self.schedule_data = {
            'weekday': None,
            'day': None,
            'hour': 10,
            'minute': 36,
            'active':'active',
            'interval': "day"
        }
        self.lecture1 = Lecture.objects.create(
            topic="OOP",
            course=self.course1,
            presentation='media/pop_y1PlE5O.pdf',
            schedule=self.schedule_data
        )
        self.lecture2 = Lecture.objects.create(
            topic="POP",
            course=self.course2,
            presentation='media/pop_y1PlE5O.pdf',
            schedule=self.schedule_data
        )
        self.url = LectureUrls.lecture_api_view_url

    def test_lecture_retrieve_teacher_success(self):
        self.client.login(username='teacher', password='password')
        response = self.client.get(f'{self.url}{self.lecture1.uuid}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lecture_retrieve_student_success(self):
        self.client.login(username='student', password='password')
        response = self.client.get(f'{self.url}{self.lecture1.uuid}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lecture_retrieve_teacher_failure(self):
        self.client.login(username='teacher', password='password')
        response = self.client.get(f'{self.url}{self.lecture2.uuid}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_lecture_retrieve_student_failure(self):
        self.client.login(username='student', password='password')
        response = self.client.get(f'{self.url}{self.lecture2.uuid}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_lecture_update_teacher_success(self):
        self.client.login(username='teacher', password='password')
        presentation_file = SimpleUploadedFile(
            "pop_y1PlE5O.pdf",
            b"file_content",
            content_type="application/pdf"
        )
        data = {
            'topic': 'Python',
            'course': str(self.course1.uuid),
            'presentation': presentation_file,
            'schedule.weekday': '',
            'schedule.day': '',
            'schedule.hour': 10,
            'schedule.minute': 36,
            'schedule.active': 'active',
            'schedule.interval': 'day',
        }
        response = self.client.put(f'{self.url}{self.lecture1.uuid}/', data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['topic'],'Python')

    def test_lecture_update_student_failure(self):
        self.client.login(username='student', password='password')
        presentation_file = SimpleUploadedFile(
            "pop_y1PlE5O.pdf",
            b"file_content",
            content_type="application/pdf"
        )
        data = {
            'topic': 'Python',
            'course': str(self.course1.uuid),
            'presentation': presentation_file,
            'schedule.weekday': '',
            'schedule.day': '',
            'schedule.hour': 10,
            'schedule.minute': 36,
            'schedule.active': 'active',
            'schedule.interval': 'day',
        }
        response = self.client.put(f'{self.url}{self.lecture1.uuid}/', data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lecture_delete_teacher_success(self):
        self.client.login(username='teacher', password='password')
        response = self.client.delete(f'{self.url}{self.lecture1.uuid}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_lecture_delete_student_failure(self):
        self.client.login(username='student', password='password')
        response = self.client.delete(f'{self.url}{self.lecture1.uuid}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
