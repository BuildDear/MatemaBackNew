# from MatemaBackNew.Manager.serializer import ThemeCreateSerializer, ThemeSerializer
from django.db.models import Count
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.utils import timezone
from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from Task.models import DoneTask, TaskList
from Task.serializer import TaskListSerializer

# from drf_yasg.utils import swagger_auto_schema
# @swagger_auto_schema(
#         request_body=ThemeCreateSerializer,
#         responses={
#             status.HTTP_201_CREATED: ThemeSerializer(),
#             status.HTTP_400_BAD_REQUEST: 'Bad Request',
#             status.HTTP_404_NOT_FOUND: 'Theme not found'
#         }
#     )

class UserTasksView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, username, format=None):
        thirty_days_ago = timezone.now() - timedelta(days=30)
        tasks = DoneTask.objects.filter(user_id=username, is_done=True, datetime__gte=thirty_days_ago)
        serializer = TaskListSerializer(tasks, many=True)
        return Response(serializer.data)



class UserNotDoneTasksView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, username, format=None):
        all_user_tasks = TaskList.objects.filter(user_id=username)
        done_task_ids = DoneTask.objects.filter(user_id=username).values_list('task_id', flat=True)

        not_done_tasks = all_user_tasks.exclude(task_id__in=done_task_ids)

        serializer = TaskListSerializer(not_done_tasks, many=True)
        return Response(serializer.data)

class UserTaskWeekView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, username, format=None):
        # The number of completed halls for the evening day
        weekly_done_tasks = DoneTask.objects.filter(
            user_id=username,
            is_done=True,
            datetime__gte=timezone.now() - timedelta(days=7)
        ).extra({'day': 'date(datetime)'}).values('day').annotate(count=Count('id'))

        # A dictionary where the key is the day of the week and the value is the number of completed tasks
        weekly_done_tasks_dict = {entry['day']: entry['count'] for entry in weekly_done_tasks}

        # We fill with zeros the days when no task was completed
        today = timezone.now().date()
        days_of_week = [today - timedelta(days=i) for i in range(7)]
        for day in days_of_week:
            if day not in weekly_done_tasks_dict:
                weekly_done_tasks_dict[day] = 0

        # We sort the dictionary by days of the week
        sorted_weekly_done_tasks = sorted(weekly_done_tasks_dict.items())

        # We are preparing data for sending through the serializer
        result_data = [{'day': str(day), 'count': count} for day, count in sorted_weekly_done_tasks]

        return Response(result_data)