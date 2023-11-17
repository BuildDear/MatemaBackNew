from rest_framework import serializers
from django.core.exceptions import ValidationError
from Task.models import Task, Theme, TypeAnswer

from User.models import User


class TaskSerializer(serializers.ModelSerializer):
    """List of Task"""

    class Meta:
        model = Task
        fields = "__all__"


class ThemeSerializer(serializers.ModelSerializer):
    """List of Theme"""

    class Meta:
        model = Theme
        fields = "__all__"


class TaskCreateSerializer(serializers.ModelSerializer):
    theme = ThemeSerializer()

    class Meta:
        model = Task
        fields = "__all__"

    def create(self, validated_data):
        # Перевіряємо, чи існує завдання з таким самим іменем
        if Task.objects.filter(name=validated_data['name']).exists():
            raise serializers.ValidationError({'name': 'A task with that name already exists.'})

        # Перевіряємо, чи існують записи для Theme та TypeAnswer
        if not Theme.objects.filter(id=validated_data['theme']).exists():
            raise serializers.ValidationError({'theme': 'Invalid theme_id'})

        if not TypeAnswer.objects.filter(id=validated_data['type_ans']).exists():
            raise serializers.ValidationError({'type_ans': 'Invalid type_id'})

        # Створюємо і зберігаємо нове завдання
        task = Task.objects.create(**validated_data)

        return task


class ThemeCreateSerializer(serializers.ModelSerializer):

    def create_theme(self, name):
        if Theme.objects.filter(id=name).exists():
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


class UserListSerializer(serializers.ModelSerializer):
    """List of users"""

    class Meta:
        model = User
        fields = "__all__"


class UserDetailSerializer(serializers.ModelSerializer):
    """All user"""

    class Meta:
        model = User
        fields = "__all__"
