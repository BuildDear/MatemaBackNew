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

        try:
            task = Task.objects.get(name=task_name)
        except Task.DoesNotExist:
            return Response({'message': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

        DoneTask.objects.create(
            user=user,
            task=task,
            is_done=True
        )

        return Response({"message": "Задача успішно перенесена"}, status=status.HTTP_200_OK)