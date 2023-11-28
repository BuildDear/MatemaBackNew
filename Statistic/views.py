from rest_framework.permissions import AllowAny
from django.utils import timezone
from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from Task.models import DoneTask
from Task.serializer import TaskListSerializer


class UserTasksView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, user_id, format=None):
        thirty_days_ago = timezone.now() - timedelta(days=30)
        tasks = DoneTask.objects.filter(user_id=user_id, is_done=True, datetime__gte=thirty_days_ago)
        serializer = TaskListSerializer(tasks, many=True)
        return Response(serializer.data)
