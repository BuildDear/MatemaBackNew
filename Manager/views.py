from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework import status
from .serializer import *
from Task.models import *
from rest_framework.response import Response


class TaskView(APIView):
    permission_classes = (AllowAny,)

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
