from django.core.files.storage import default_storage
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from .serializer import *
from Task.models import *
from User.models import *
from rest_framework.response import Response


class TaskView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        task = Task.objects.all()
        serializer = TaskSerializer(task, many=True)
        return Response(serializer.data)


class TaskSearchView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        theme_id = request.query_params.get('theme_id')
        point = request.query_params.get('point')

        if theme_id and point:
            tasks = Task.objects.filter(theme_id=theme_id, point=point)
        elif theme_id:
            tasks = Task.objects.filter(theme_id=theme_id)
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
        task_id = kwargs.get('pk', None)
        if task_id is not None:
            try:
                task = Task.objects.get(id=task_id)
                task.delete()
                return Response({"message": "Successful delete!"}, status=status.HTTP_204_NO_CONTENT)
            except Task.DoesNotExist:
                return Response({"message": "Invalid task_id."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "Task ID is required."}, status=status.HTTP_400_BAD_REQUEST)


class TaskEditView(APIView):
    permission_classes = (AllowAny,)

    def put(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response({'message': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response({'message': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TaskSerializer(task, data=request.data, partial=True)
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
        theme_id = kwargs.get('pk')
        if theme_id is not None:
            try:
                theme = Theme.objects.get(id=theme_id)
                theme.delete()
                return Response({"message": "Successful delete!"}, status=status.HTTP_204_NO_CONTENT)
            except Theme.DoesNotExist:
                return Response({"message": "Invalid theme_id."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "theme_id is required."}, status=status.HTTP_400_BAD_REQUEST)


class ThemeEditView(APIView):
    permission_classes = (AllowAny,)

    def put(self, request, pk):
        try:
            theme = Theme.objects.get(pk=pk)
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


class TaskAnswerCreateView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response({'message': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TaskAnswerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        answer_data = serializer.validated_data['answer_data']

        # Determine the answer type based on the provided JSON structure
        answer_type = None
        if 'options' in answer_data and 'correct_answer' in answer_data:
            answer_type = 'mcq'
        elif 'pairs' in answer_data:
            answer_type = 'matching'
        elif 'correct_answer' in answer_data:
            answer_type = 'short'

        # Check if the determined answer type matches the type_ans of the task
        if answer_type != task.type_ans.name:
            return Response({'message': 'Invalid answer data structure for the task type'}, status=status.HTTP_400_BAD_REQUEST)

        # Set the new answer based on the determined answer_type
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

        task.save()

        return Response({'message': 'Answer added successfully'}, status=status.HTTP_200_OK)


class TaskTypeSetView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response({'message': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TaskTypeSetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get the TypeAnswer instance from the validated data
        type_ans_instance = serializer.validated_data['type_ans']

        # Set the new type_ans and delete existing answer data
        task.type_ans = type_ans_instance
        task.answer_matching = None
        task.answer_short = None
        task.answer_mcq = None

        task.save()

        return Response({'message': 'Type_ans set successfully and existing answer data deleted'}, status=status.HTTP_200_OK)

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
