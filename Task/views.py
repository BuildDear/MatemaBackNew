from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from .serializers import *


class TaskCreateView(APIView):
    @staticmethod
    def create_task(request, *args, **kwargs):
        serializer = TaskCreateSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.create_task(serializer.validated_data)
            return JsonResponse(TaskCreateSerializer(task).data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDeleteView(APIView):
    @staticmethod
    def delete_task(request, *args, **kwargs):
        # Ваш серіалізатор очікує 'id', тому ми отримаємо 'task_id' з 'kwargs'
        task_id = kwargs.get('task_id', None)
        if task_id is not None:
            # Створюємо екземпляр серіалізатора з даними запиту
            serializer = TaskDeleteSerializer(data={'id': task_id})
            # Перевіряємо, чи валідний 'id'
            if serializer.is_valid():
                result = serializer.delete_task(task_id)
                if result == "Successful delete!":
                    return JsonResponse({"message": result}, status=status.HTTP_204_NO_CONTENT)
                else:
                    return JsonResponse({"message": result}, status=status.HTTP_404_NOT_FOUND)
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse({"message": "Task ID is required."}, status=status.HTTP_400_BAD_REQUEST)


class ThemCreateView(APIView):
    @staticmethod
    def create_them(request, *args, **kwargs):
        # Витягуємо ім'я з даних запиту
        name = request.data.get('name')
        # Перевіряємо, чи ім'я було надано
        if name:
            # Створюємо Them за допомогою серіалізатора
            them = ThemCreateSerializer.create_them(name)
            # Повертаємо серіалізовані дані новоствореного Them
            serializer = ThemCreateSerializer(them)
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(
                {"message": "Name is required for creating a Them."},
                status=status.HTTP_400_BAD_REQUEST
            )


class ThemDeleteView(APIView):
    @staticmethod
    def delete(request, *args, **kwargs):
        them_id = kwargs.get('them_id')
        if them_id is None:
            return JsonResponse({'message': 'Missing them_id.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ThemDeleteSerializer(data={'id': them_id})
        if serializer.is_valid(raise_exception=True):
            try:
                result = serializer.delete_them(them_id)
                return JsonResponse(result, status=status.HTTP_204_NO_CONTENT)
            except ValidationError as e:
                return JsonResponse({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
