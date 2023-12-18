from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from rest_framework import status

from rest_framework.test import APIClient


class AccountActivationTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        user_data = {
            "username": "MarikLNU_matema",
            "first_name": "Maria",
            "last_name": "Maria1",
            "email": "matema.group@gmail.com",
            "password": "OLGGG1234olggg!!!***1234",
            "re_password": "OLGGG1234olggg!!!***1234"
        }
        response = self.client.post('/auth/users/', user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)

        self.user = get_user_model().objects.get(username=user_data['username'])
        self.uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.token = default_token_generator.make_token(self.user)

    def test_activate_account_success(self):
        response = self.client.post('/activate_account/', {'uidb64': self.uid, 'token': self.token})
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)
        self.assertEqual(response.status_code, 200)

    def test_activate_account_invalid_token(self):
        response = self.client.post('/activate_account/', {'uidb64': self.uid, 'token': 'wrong-token'})
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)
        self.assertEqual(response.status_code, 400)

    def test_activate_account_invalid_uid(self):
        response = self.client.post('/activate_account/', {'uidb64': 'wrong-uid', 'token': self.token})
        self.assertEqual(response.status_code, 404)
#
# class UserActiveCheckTests(TestCase):
#
#     def setUp(self):
#         user_data = {
#             "username": "MarikLNU_matema",
#             "first_name": "Maria",
#             "last_name": "Maria1",
#             "email": "matema.group@gmail.com",
#             "password": "OLGGG1234olggg!!!***1234",
#             "re_password": "OLGGG1234olggg!!!***1234"
#         }
#         response = self.client.post('/auth/users/', user_data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
#
#         # Отримання JWT токенів
#         response = self.client.post('/auth/jwt/create/', {
#             "username": "MarikLNU_matema",
#             "password": "OLGGG1234olggg!!!***1234"
#         }, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
#         self.token = response.data['access']
#         self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
#
#     def test_check_active_user(self):
#         response = self.client.get(f'/check-user-active/{self.active_user.username}/')
#         self.assertEqual(response.status_code, 200)
#
#     def test_check_inactive_user(self):
#         response = self.client.get(f'/check-user-active/{self.inactive_user.username}/')
#         self.assertEqual(response.status_code, 401)
#
#     def test_check_nonexistent_user(self):
#         response = self.client.get('/check-user-active/nonexistentuser/')
#         self.assertEqual(response.status_code, 404)
