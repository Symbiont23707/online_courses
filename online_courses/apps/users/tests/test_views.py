from django.contrib.auth.hashers import check_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from urllib.parse import urlencode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import status
from rest_framework.test import APITestCase
from apps.users.models import User
from libs.types import UserUrls, RoleTypes


class PasswordResetViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', email='test@example.com')

    def test_password_reset_view_success(self):
        data = {'email': 'test@example.com'}
        response = self.client.post(UserUrls.reset_url, data, format='json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_password_reset_view_failure(self):
        data = {'email': 'test1@example.com'}
        response = self.client.post(UserUrls.reset_url, data, format='json')
        self.assertNotEquals(response.status_code, status.HTTP_201_CREATED)


class ChangePasswordViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username='testuser', email='test@example.com')
        self.user.set_password("old_password")
        self.user.save()
        self.token = PasswordResetTokenGenerator().make_token(self.user)
        self.encoded_uuid = urlsafe_base64_encode(force_bytes(self.user.uuid))
        self.query_string = urlencode(dict(token=self.token, encoded_uuid=self.encoded_uuid))
        self.url = f'{UserUrls.change_url}{self.query_string}'

    def test_change_password_view_success(self):
        data = {
            'password': 'pass1',
            'password_confirm': 'pass1',
        }
        response = self.client.post(self.url, data, format='json')
        self.user.refresh_from_db()
        self.assertEquals(check_password(data['password'], self.user.password), True)

    def test_change_password_view_failure(self):
        data = {
            'password': 'pass1',
            'password_confirm': '123',
        }
        response = self.client.post(self.url, data, format='json')
        self.user.refresh_from_db()
        self.assertNotEquals(check_password(data['password'], self.user.password), True)



class InviteViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username='testuser', email='test@example.com', password='testpassword')
        self.url = UserUrls.invite_url

    def test_invite_view_success(self):
        data = {
            'email': 'test4@example.com',
            'username': '2testuser',
            'password':'testpassword',
            'role': RoleTypes.Teacher
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invite_view_failure(self):
        data = {
            'email': 'test2@example.com',
            'username': 'testuser',
            'password': 'testpassword',
            'role': RoleTypes.Teacher
        }
        response = self.client.post(self.url, data, format='json')
        self.assertNotEquals(response.status_code, status.HTTP_201_CREATED)
