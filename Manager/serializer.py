from rest_framework import serializers
from Task.models import Task, TypeAnswer, Theme
from django.core.exceptions import ValidationError


class TaskSerializer(serializers.ModelSerializer):
    """List of Task"""

    class Meta:
        model = Task
        fields = "__all__"


class TaskCreateSerializer(serializers.ModelSerializer):

    def create_task(self, validated_data):
        # Отримуємо дані з validated_data замість окремих аргументів
        name = validated_data.get('name')
        text = validated_data.get('text')
        image_url = validated_data.get('image_url')
        point = validated_data.get('point')
        theme_id = validated_data.get('theme')
        type_id = validated_data.get('type')
        answer = validated_data.get('answer')

        # Перевіряємо, чи існує завдання з таким самим іменем
        if Task.objects.filter(name=name).exists():
            raise ValidationError('A task with that name already exists.')

        # Перевіряємо, чи існують записи для Them та TypeAnswer
        try:
            theme = Theme.objects.get(id=theme_id)
            type_answer = TypeAnswer.objects.get(id=type_id)
        except Theme.DoesNotExist:
            raise ValidationError('Invalid theme_id')
        except TypeAnswer.DoesNotExist:
            raise ValidationError('Invalid type_id')

        # Створюємо і зберігаємо нове завдання
        task = Task.objects.create(
            name=name,
            text=text,
            image_url=image_url,
            point=point,
            theme=theme,
            type=type_answer,
            answer=answer
        )
        return task

    class Meta:
        model = Task
        fields = "__all__"


class ThemeCreateSerializer(serializers.ModelSerializer):

    def create_theme(self, name):
        if Theme.objects.filter(name=name).exists():
            raise ValidationError('A theme with that name already exists.')

        # Creates a new Them instance and saves it to the database
        theme = Theme.objects.create(name=name)
        return theme

    class Meta:
        model = Theme
        fields = ['name']


class ThemeSerializer(serializers.ModelSerializer):
    """List of Theme"""

    class Meta:
        model = Theme
        fields = "__all__"
