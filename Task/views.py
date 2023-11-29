from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework import status
from User.models import *
from rest_framework.response import Response
from Task.serializer import *


class TaskListView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        username = request.data.get('username')
        # Перевірка, чи вказано username
        if not username:
            return Response({"error": "Username is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Створення списку завдань для користувача
            tasklist = create_tasklist(username)

            # Серіалізація даних списку завдань
            serializer = TaskListSerializer(tasklist, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Для відловлення інших можливих помилок
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TransferTaskView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, username):
        user = User.objects.get(username=username)
        task_name = request.data.get('name')
        user_answer_data = request.data.get('user_answer')  # Отримання даних відповіді користувача

        try:
            task = Task.objects.get(name=task_name)
        except Task.DoesNotExist:
            return Response({'message': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

        if not TaskList.objects.filter(user=user, task=task).exists():
            return Response({'message': 'Task and user combination not found in TaskList'},
                            status=status.HTTP_404_NOT_FOUND)

        # Перевірка відповіді користувача
        if not self.is_correct_answer(task, user_answer_data):
            return Response({'message': 'Incorrect answer'}, status=status.HTTP_400_BAD_REQUEST)

        DoneTask.objects.create(
            user=user,
            task=task,
            is_done=True
        )

        return Response({"message": "Task transfer successfully"}, status=status.HTTP_200_OK)

    def is_correct_answer(self, task, user_answer_data):
        # Перевірка типу відповіді і порівняння з відповідями в базі даних
        if (task.answer_mcq or task.answer_short) and 'correct_answer' in user_answer_data:
            return True
        return False

