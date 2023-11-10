from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from Task.serializers import *
from Task.models import *
from rest_framework import generics


class TasksView(APIView):
    def get(self, request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return JsonResponse(serializer.data)


class TaskCreateView(APIView):
    def create(self, request, *args, **kwargs):
        serializer = TaskCreateSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.create_task(serializer.validated_data)
            return JsonResponse(TaskCreateSerializer(task).data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDeleteView(APIView):
    def delete(self, request, *args, **kwargs):
        task_id = kwargs.get('task_id', None)
        if task_id is not None:
            try:
                task = Task.objects.get(id=task_id)
                task.delete()
                return JsonResponse({"message": "Successful delete!"}, status=status.HTTP_204_NO_CONTENT)
            except Task.DoesNotExist:
                return JsonResponse({"message": "Invalid task_id."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return JsonResponse({"message": "Task ID is required."}, status=status.HTTP_400_BAD_REQUEST)


class TaskEditView(generics.RetrieveUpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class ThemeView(APIView):
    def get(self, request):
        theme = Theme.objects.all()
        serializer = ThemeSerializer(theme, many=True)
        return JsonResponse(serializer.data)


class ThemeCreateView(APIView):
    def create(self, request):
        serializer = ThemeCreateSerializer(data=request.data)
        if serializer.is_valid():
            theme = serializer.create_theme(serializer.validated_data)
            return JsonResponse(ThemeCreateSerializer(theme).data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ThemeDeleteView(APIView):
    def delete(self, request, **kwargs):
        theme_id = kwargs.get('them_id')
        if theme_id is not None:
            try:
                theme = Theme.objects.get(id=theme_id)
                theme.delete()
                return JsonResponse({"message": "Successful delete!"}, status=status.HTTP_204_NO_CONTENT)
            except Theme.DoesNotExist:
                return JsonResponse({"message": "Invalid theme_id."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return JsonResponse({"message": "theme_id is required."}, status=status.HTTP_400_BAD_REQUEST)


class ThemeEditView(generics.RetrieveUpdateAPIView):
    queryset = Theme.objects.all()
    serializer_class = ThemeSerializer
