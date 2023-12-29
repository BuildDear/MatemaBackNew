from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from Task.models import *
from .serializer import TaskSerializer


class TaskViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Створення тестових даних
        cls.tasks = [
            Task.objects.create(
                name=f'Task {i}',
                text='Sample Text',
                point=i,
                theme=Theme.objects.create(name='Sample Theme'),
                type_ans=TypeAnswer.objects.get_or_create(id=1),
                photo=None,
                answer_matching=None,
                answer_short=None,
                answer_mcq=None
                # інші поля, якщо потрібно
            ) for i in range(3)
        ]

    def test_get_task_list(self):
        # URL для вашого TaskView
        url = reverse('view-task')# Замініть 'task-list' на назву вашого URL

        # Виконання GET запиту
        response = self.client.get(url)

        # Перевірка статусу відповіді
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Перевірка даних, повернених у відповіді
        expected_data = TaskSerializer(self.tasks, many=True).data
        self.assertEqual(response.data, expected_data)

