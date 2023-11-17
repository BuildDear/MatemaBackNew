from django.http import JsonResponse
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from .serializer import *

from rest_framework import generics

from User.models import User


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


class UserListView(ListAPIView):
    """
    API view to list all users.

    This view extends Django REST Framework's ListAPIView to provide a list of all users.
    It is intended to be used by clients to retrieve a list of all user accounts.

    Attributes:
    - permission_class: This view requires the user to be authenticated to access it.
      'IsAuthenticated' ensures that only authenticated users can make requests to this view.
    - queryset: The set of user records that this view will handle. Here, it's set to include all users in the User model.
    - serializer_class: The serializer class used to convert user instances into a format that can be easily rendered into JSON.
    """

    permission_class = IsAuthenticated
    queryset = User.objects.all()
    serializer_class = UserListSerializer


class UserDetailView(RetrieveAPIView):
    """
    API view to retrieve a single user's details.

    This view extends Django REST Framework's RetrieveAPIView to provide details of a specific user.
    It is used to retrieve the details of a single user account, identified by the user's ID in the URL.

    Attributes:
    - queryset: The set of user records that this view will handle. As with UserListView, it includes all users.
    - serializer_class: The serializer class used for converting the user instance into a format that can be rendered into JSON.
    """

    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
