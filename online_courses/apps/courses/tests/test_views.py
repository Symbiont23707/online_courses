from rest_framework import status
from rest_framework.test import APITestCase
from apps.courses.models import Course
from apps.users.models import Teacher, Student, User
from libs.types import CourseUrls

class CourseAPIViewTest(APITestCase):
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
            )
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
        self.url = CourseUrls.course_api_view_url

    def test_list_courses_from_teacher_success(self):
        self.client.login(username='teacher', password='password')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_courses_from_student_success(self):
        self.client.login(username='student', password='password')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_course_success(self):
        self.client.login(username='teacher', password='password')
        data = {
            'name': 'Kotlin',
            'specialty': 'Programming',
            'teachers': [str(self.teacher.uuid)],
            'students': [str(self.student.uuid)],
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_course = Course.objects.get(name='Kotlin')
        self.assertIsNotNone(created_course)

    def test_create_course_failure(self):
        self.client.login(username='student', password='password')
        data = {
            'name': 'Kotlin',
            'specialty': 'Programming',
            'teachers': [str(self.teacher.uuid)],
            'students': [str(self.student.uuid)],
        }
        response = self.client.post(self.url, data, format='json')
        self.assertNotEquals(response.status_code, status.HTTP_201_CREATED)

class CourseDetailAPIViewTest(APITestCase):
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
            )
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
        self.url = CourseUrls.course_api_view_url

    def test_course_retrieve_teacher_success(self):
        self.client.login(username='teacher', password='password')
        response = self.client.get(f'{self.url}{self.course1.uuid}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_course_retrieve_student_success(self):
        self.client.login(username='student', password='password')
        response = self.client.get(f'{self.url}{self.course1.uuid}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_course_retrieve_teacher_failure(self):
        self.client.login(username='teacher', password='password')
        response = self.client.get(f'{self.url}{self.course2.uuid}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_course_retrieve_student_failure(self):
        self.client.login(username='student', password='password')
        response = self.client.get(f'{self.url}{self.course2.uuid}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_course_teacher_success(self):
        self.client.login(username='teacher', password='password')
        updated_data = {
            'name': 'Python3.10',
            'specialty': 'Programming',
            'teachers': [self.teacher.uuid],
            'students': [self.student.uuid]
        }
        response = self.client.put(f'{self.url}{self.course1.uuid}/', updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Python3.10')

    def test_update_course_student_failure(self):
        self.client.login(username='student', password='password')
        updated_data = {
            'name': 'Python3.10',
            'specialty': 'Programming',
            'teachers': [self.teacher.uuid],
            'students': [self.student.uuid]
        }
        response = self.client.put(f'{self.url}{self.course1.uuid}/', updated_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_course_delete_teacher_success(self):
        self.client.login(username='teacher', password='password')
        response = self.client.delete(f'{self.url}{self.course1.uuid}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_course_delete_student_failure(self):
        self.client.login(username='student', password='password')
        response = self.client.delete(f'{self.url}{self.course1.uuid}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
