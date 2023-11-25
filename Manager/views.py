from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from .serializer import *
from Task.models import *
from User.models import *
from rest_framework.response import Response
from Task.logic import create_tasklist


class TaskView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        task = Task.objects.all()
        serializer = TaskSerializer(task, many=True)
        return Response(serializer.data)


class TaskSearchView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        theme_name = request.query_params.get('theme_id')
        point = request.query_params.get('point')

        if theme_name and point:
            tasks = Task.objects.filter(theme_id=theme_name, point=point)
        elif theme_name:
            tasks = Task.objects.filter(theme_id=theme_name)
        elif point:
            tasks = Task.objects.filter(point=point)
        else:
            return Response({"message": "Invalid or missing parameters."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TaskCreateView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = TaskCreateSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save()
            return Response(TaskCreateSerializer(task).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDeleteView(APIView):
    permission_classes = (AllowAny,)

    def delete(self, request, **kwargs):
        task_name = kwargs.get('name', None)
        if task_name is not None:
            try:
                task = Task.objects.get(name=task_name)
                task.delete()
                return Response({"message": "Successful delete!"}, status=status.HTTP_204_NO_CONTENT)
            except Task.DoesNotExist:
                return Response({"message": "Invalid task_id."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "Task ID is required."}, status=status.HTTP_400_BAD_REQUEST)


class TaskEditView(APIView):
    permission_classes = (AllowAny,)

    def put(self, request, name):
        try:
            task = Task.objects.get(name=name)
        except Task.DoesNotExist:
            return Response({'message': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TaskUpdateSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, name):
        try:
            task = Task.objects.get(name=name)
        except Task.DoesNotExist:
            return Response({'message': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TaskUpdateSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ThemeView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        theme = Theme.objects.all()
        serializer = ThemeSerializer(theme, many=True)
        return Response(serializer.data)


class ThemeCreateView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = ThemeCreateSerializer(data=request.data)
        if serializer.is_valid():
            theme = serializer.save()
            return Response(ThemeCreateSerializer(theme).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ThemeDeleteView(APIView):
    permission_classes = (AllowAny,)

    def delete(self, request, **kwargs):
        theme_name = kwargs.get('name')
        if theme_name is not None:
            try:
                theme = Theme.objects.get(name=theme_name)
                theme.delete()
                return Response({"message": "Successful delete!"}, status=status.HTTP_204_NO_CONTENT)
            except Theme.DoesNotExist:
                return Response({"message": "Invalid theme_id."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "theme_id is required."}, status=status.HTTP_400_BAD_REQUEST)


class ThemeEditView(APIView):
    permission_classes = (AllowAny,)

    def put(self, request, name):
        try:
            theme = Theme.objects.get(name=name)
        except Theme.DoesNotExist:
            return Response({'message': 'Theme not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ThemeSerializer(theme, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TypeAnswerView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        type_ans = TypeAnswer.objects.all()
        serializer = TypeAnswerSerializer(type_ans, many=True)
        return Response(serializer.data)


class TypeAnswerCreateView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TypeAnswerCreateSerializer(data=request.data)
        if serializer.is_valid():
            type_ans = serializer.save()
            return Response(ThemeCreateSerializer(type_ans).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TypeAnswerDeleteView(APIView):
    permission_classes = (AllowAny,)

    def delete(self, request, **kwargs):
        type_ans_id = kwargs.get('pk')
        if type_ans_id is not None:
            try:
                type_ans = TypeAnswer.objects.get(id=type_ans_id)
                type_ans.delete()
                return Response({"message": "Successful delete!"}, status=status.HTTP_204_NO_CONTENT)
            except Theme.DoesNotExist:
                return Response({"message": "Invalid type_ans_id."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "type_ans_id is required."}, status=status.HTTP_400_BAD_REQUEST)


class TypeAnswerEditView(APIView):
    permission_classes = (AllowAny,)

    def put(self, request, pk):
        try:
            type_ans = TypeAnswer.objects.get(pk=pk)
        except TypeAnswer.DoesNotExist:
            return Response({'message': 'Type answer not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TypeAnswerSerializer(type_ans, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserThemeCreateView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserThemeCreateSerializer(data=request.data)
        if serializer.is_valid():
            user_theme = serializer.save()
            return Response(UserThemeCreateSerializer(user_theme).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

#################################


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
