from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class UserTasksViewTest(TestCase):
    def test_user_tasks_view(self):
        username = 'test_user'
        url = reverse('user-task-done', args=[username])
        client = APIClient()

        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class UserNotDoneTasksViewTest(TestCase):

    def test_user_not_done_tasks_view(self):
        username = 'test_user'
        url = reverse('user-task-not-done', args=[username])
        client = APIClient()

        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class UserTaskWeekViewTest(TestCase):
    def test_user_task_week_view(self):
        username = 'test_user'
        url = reverse('user-task-week', args=[username])
        client = APIClient()

        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
