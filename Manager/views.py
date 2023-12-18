from django.core.files.storage import default_storage
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from .serializer import *
from rest_framework.response import Response
from Task.serializer import *
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class TaskView(APIView):
    permission_classes = (AllowAny,)
    # permission_classes = (IsAuthenticated,)

    def get(self, request):
        # Retrieve all tasks from the database
        task = Task.objects.all()
        serializer = TaskSerializer(task, many=True)
        return Response(serializer.data)


class TaskSearchView(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('theme', openapi.IN_QUERY, description="Theme ID", type=openapi.TYPE_STRING),
            openapi.Parameter('point', openapi.IN_QUERY, description="Point value", type=openapi.TYPE_INTEGER)
        ],
        responses={status.HTTP_200_OK: TaskSerializer(many=True)}
    )

    def get(self, request):
        # Extract parameters from the request
        theme_name = request.query_params.get('theme')
        point = request.query_params.get('point')

        # Filter tasks based on provided query parameters
        if theme_name and point:
            tasks = Task.objects.filter(theme_id=theme_name, point=point)
        elif theme_name:
            tasks = Task.objects.filter(theme_id=theme_name)
        elif point:
            tasks = Task.objects.filter(point=point)
        else:
            # Respond with an error message if required parameters are missing
            return Response({"message": "Invalid or missing parameters."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TaskCreateView(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        request_body=TaskCreateSerializer,
        responses={
            status.HTTP_201_CREATED: ThemeCreateSerializer(),
            status.HTTP_400_BAD_REQUEST: 'Bad Request'
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = TaskCreateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        task = serializer.save()

        # Обробка додаткових даних для завдання
        answer_data = request.data.get('answer_data')
        if answer_data:
            type_ans_id = request.data.get('type_ans')
            if not type_ans_id:
                task.delete()
                return Response({'message': 'Type_ans must be specified when adding an answer'},
                                status=status.HTTP_400_BAD_REQUEST)

            try:
                type_ans_instance = TypeAnswer.objects.get(id=type_ans_id)
            except TypeAnswer.DoesNotExist:
                task.delete()
                return Response({'message': 'Invalid type_ans ID'},
                                status=status.HTTP_400_BAD_REQUEST)

            # Встановлення відповідного типу відповіді
            answer_type = self.determine_answer_type(answer_data)
            task = self.set_task_answer(task, answer_type, answer_data)
            task.type_ans = type_ans_instance
            task.save()

        return Response(TaskCreateSerializer(task).data, status=status.HTTP_201_CREATED)

    def determine_answer_type(self, answer_data):
        if 'options' in answer_data and 'correct_answer' in answer_data:
            return 'mcq'
        elif 'pairs' in answer_data:
            return 'matching'
        elif 'correct_answer' in answer_data:
            return 'short'
        return None

    def set_task_answer(self, task, answer_type, answer_data):
        if answer_type == 'mcq':
            task.answer_matching = None
            task.answer_short = None
            task.answer_mcq = answer_data
        elif answer_type == 'matching':
            task.answer_mcq = None
            task.answer_short = None
            task.answer_matching = answer_data
        elif answer_type == 'short':
            task.answer_mcq = None
            task.answer_matching = None
            task.answer_short = answer_data
        return task


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

    @swagger_auto_schema(
        request_body=TaskUpdateSerializer,
        responses={
            status.HTTP_201_CREATED: TaskUpdateSerializer(),
            status.HTTP_400_BAD_REQUEST: 'Bad Request',
            status.HTTP_404_NOT_FOUND: 'Task not found'
        }
    )
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

    @swagger_auto_schema(
        request_body=ThemeCreateSerializer,
        responses={
            status.HTTP_201_CREATED: ThemeCreateSerializer(),
            status.HTTP_400_BAD_REQUEST: 'Bad Request'
        }
    )
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

    @swagger_auto_schema(
        request_body=ThemeSerializer,
        responses={
            status.HTTP_201_CREATED: ThemeSerializer(),
            status.HTTP_400_BAD_REQUEST: 'Bad Request',
            status.HTTP_404_NOT_FOUND: 'Theme not found'
        }
    )
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

    @swagger_auto_schema(
        request_body=TypeAnswerCreateSerializer,
        responses={
            status.HTTP_201_CREATED: TypeAnswerCreateSerializer(),
            status.HTTP_400_BAD_REQUEST: 'Bad Request'
        }
    )

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

    @swagger_auto_schema(
        request_body=TypeAnswerSerializer,
        responses={
            status.HTTP_201_CREATED: TypeAnswerSerializer(),
            status.HTTP_400_BAD_REQUEST: 'Bad Request',
            status.HTTP_404_NOT_FOUND: 'Type answer not found'
        }
    )
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
            user_themes = serializer.save()
            return Response(UserThemeCreateSerializer(user_themes, many=True).data, status=status.HTTP_201_CREATED)
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


class TaskPhotoCreateView(APIView):
    permission_classes = (AllowAny,)
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response({'message': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

        if task.photo:
            task.photo.delete()

        photo = request.data.get('photo')

        # Extract the original file extension
        original_extension = photo.name.split('.')[-1]

        # Generate a new file name with the original extension
        file_name = f"{task.name}_ID{task.id}.{original_extension}"

        # Save the photo with the new file name
        task.photo.save(file_name, photo)

        serializer = TaskPhotoSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TaskPhotoDeleteView(APIView):
    permission_classes = (AllowAny,)

    def delete(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response({'message': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

        if task.photo:
            file_path = task.photo.path
            default_storage.delete(file_path)

            task.photo = None
            task.save()

            return Response({'message': 'Task photo deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message': 'Task does not have a photo'}, status=status.HTTP_404_NOT_FOUND)


class TaskPhotoRetrieveView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response({'message': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

        if task.photo:

            # Return the photo URL or other information
            serializer = TaskPhotoSerializer(task)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Task does not have a photo'}, status=status.HTTP_404_NOT_FOUND)



