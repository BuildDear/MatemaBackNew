from rest_framework import serializers
from .models import Task, TypeAnswer, Them
from django.core.exceptions import ValidationError
from djoser.serializers import UserCreateSerializer


class TaskSerializer(serializers.ModelSerializer):
    """List of users"""

    class Meta:
        model = Task
        fields = "__all__"


class TaskDetailSerializer(serializers.ModelSerializer):
    """All Task"""

    class Meta:
        model = Task
        fields = "__all__"


class TaskCreateSerializer(serializers.ModelSerializer):

    @staticmethod
    def create_task(validated_data):
        # Отримуємо дані з validated_data замість окремих аргументів
        name = validated_data.get('name')
        text = validated_data.get('text')
        image_url = validated_data.get('image_url')
        point = validated_data.get('point')
        them_id = validated_data.get('them')
        type_id = validated_data.get('type')
        answer = validated_data.get('answer')

        # Перевіряємо, чи існує завдання з таким самим іменем
        if Task.objects.filter(name=name).exists():
            raise ValidationError('Завдання з такою назвою вже існує.')

        # Перевіряємо, чи існують записи для Them та TypeAnswer
        try:
            them = Them.objects.get(id=them_id)
            type_answer = TypeAnswer.objects.get(id=type_id)
        except Them.DoesNotExist:
            raise ValidationError('Invalid them_id')
        except TypeAnswer.DoesNotExist:
            raise ValidationError('Invalid type_id')

        # Створюємо і зберігаємо нове завдання
        task = Task.objects.create(
            name=name,
            text=text,
            image_url=image_url,
            point=point,
            them=them,
            type=type_answer,
            answer=answer
        )
        return task

    class Meta:
        model = Task
        fields = "__all__"


class TaskDeleteSerializer(serializers.ModelSerializer):
    @staticmethod
    def delete_task(task_id):
        try:
            task = Task.objects.get(id=task_id)
            task.delete()
            return "Successful delete!"
        except Task.DoesNotExist:
            return "Invalid task_id."

    class Meta:
        model = Task
        fields = ['id']


class ThemCreateSerializer(serializers.ModelSerializer):
    @staticmethod
    def create_them(name):
        # Creates a new Them instance and saves it to the database
        them = Them.objects.create(name=name)
        return them

    class Meta:
        model = Them
        fields = ['name']


class ThemDeleteSerializer(serializers.ModelSerializer):
    @staticmethod
    def delete_them(them_id):
        try:
            # Знаходимо тему за ID і видаляємо її
            them = Them.objects.get(id=them_id)
            them.delete()
            return {'message': 'Them success delete.'}
        except Them.DoesNotExist:
            # Якщо тему не знайдено, викидаємо помилку
            raise ValidationError('Invalid them_id.')

    class Meta:
        model = Them
        fields = ['id']
