from django.test import TestCase
from rest_framework import status

from User.models import User


class UserActiveCheckTests(TestCase):

    def setUp(self):
        active_user_data = {
            "username": "MarikLNU_matema11",
            "first_name": "Maria",
            "last_name": "Maria1",
            "email": "matema.group1@gmail.com",
            "password": "OLGGG1234olggg!!!***1234",
            "re_password": "OLGGG1234olggg!!!***1234"
        }
        response = self.client.post('/auth/users/', active_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, 'Failed to create active user')
        self.active_user = User.objects.get(username="MarikLNU_matema")

        response = self.client.post('/auth/jwt/create/', {
            "username": "MarikLNU_matema",
            "password": "OLGGG1234olggg!!!***1234"
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Failed to obtain JWT token')
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_check_active_user(self):
        response = self.client.get(f'/check-user-active/{self.active_user.username}/')
        self.assertEqual(response.status_code, 200, 'Active user check failed')

    def test_check_inactive_user(self):
        response = self.client.get(f'/check-user-active/{self.inactive_user.username}/')
        self.assertEqual(response.status_code, 401, 'Inactive user check failed or wrong status code')

    def test_check_nonexistent_user(self):
        response = self.client.get('/check-user-active/nonexistentuser/')
        self.assertEqual(response.status_code, 404, 'Nonexistent user check failed')
