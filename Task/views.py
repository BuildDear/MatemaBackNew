from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework import status
from User.models import *
from rest_framework.response import Response
from Task.serializer import *


class TaskListView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, username):

        if not username:
            return Response({"error": "Username is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            tasklist = create_tasklist(username)
            serializer = TaskListSerializer(tasklist, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TransferTaskView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, username):
        user = User.objects.get(username=username)
        task_name = request.data.get('name')
        user_answer = request.data.get('user_answer')

        try:
            task = Task.objects.get(name=task_name)
        except Task.DoesNotExist:
            return Response({'message': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

        if not TaskList.objects.filter(user=user, task=task).exists():
            return Response({'message': 'Task and user combination not found in TaskList'},
                            status=status.HTTP_404_NOT_FOUND)

        correct_count = self.is_correct_answer(task, user_answer)

        if not self.is_correct_answer(task, user_answer):
            return Response({'message': 'Incorrect answer'}, status=status.HTTP_400_BAD_REQUEST)

        mark = self.type_answer(task, correct_count)

        DoneTask.objects.create(
            user=user,
            task=task,
            is_done=True,
            mark=mark
        )

        return Response({"message": "Task transfer successfully"}, status=status.HTTP_200_OK)

    def is_correct_answer(self, task, user_answer):
        correct_count = 0

        if task.answer_mcq and 'correct_answer' in task.answer_mcq:
            if task.answer_mcq['correct_answer'] == user_answer:
                correct_count = 1

        elif task.answer_short and 'correct_answer' in task.answer_short:
            correct_answers = task.answer_short['correct_answer']
            if user_answer in correct_answers:
                correct_count = 2

        elif task.answer_matching and 'pairs' in task.answer_matching:
            correct_pairs = task.answer_matching['pairs']
            for pair in user_answer:
                if pair in correct_pairs:
                    correct_count += 1

        return correct_count

    def type_answer(self, task, correct_count, user):
        if task.answer_mcq:
            user.score += 1
            user.save()
            return 1
        elif task.answer_short:
            user.score += 2
            user.save()
            return 2
        elif task.answer_matching:
            user.score += min(correct_count, 3)
            user.save()
            return min(correct_count, 3)


class UserDoneTasksView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, username):
        user = User.objects.get(username=username)
        done_tasks = DoneTask.objects.filter(user=user)
        serializer = DoneTaskSerializer(done_tasks, many=True)
        return Response(serializer.data)
