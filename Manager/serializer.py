from rest_framework import serializers
from django.core.exceptions import ValidationError
from Task.models import *
from random import sample
from User.models import User


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = "__all__"


class ThemeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Theme
        fields = "__all__"


class TypeAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = TypeAnswer
        fields = "__all__"


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"

    def create(self, validated_data):
        theme = validated_data.get('theme')
        if not isinstance(theme, Theme):
            raise serializers.ValidationError('Invalid theme instance.')

        # Перевірка type_ans
        type_ans = validated_data.get('type_ans')
        if not isinstance(type_ans, TypeAnswer):
            raise serializers.ValidationError('Invalid type_ans instance.')

        task = Task.objects.create(**validated_data)
        return task


class ThemeCreateSerializer(serializers.ModelSerializer):

    def create_theme(self, name):
        if Theme.objects.filter(id=name).exists():
            raise ValidationError('A theme with that name already exists.')

        theme = Theme.objects.create(name=name)
        return theme

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


class TypeAnswerCreateSerializer(serializers.ModelSerializer):

    def create_type_answer(self, name):
        if TypeAnswer.objects.filter(id=name).exists():
            raise ValidationError('A TypeAnswer with that name already exists.')

        type_ans = TypeAnswer.objects.create(name=name)
        return type_ans

    class Meta:
        model = TypeAnswer
        fields = "__all__"


class UserThemeCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserTheme
        fields = "__all__"

    def create(self, validated_data):
        theme = validated_data.get('theme')
        if not isinstance(theme, Theme):
            raise serializers.ValidationError('Invalid theme instance.')

        theme = validated_data.get('theme')
        if not isinstance(theme, Theme):
            raise serializers.ValidationError('Invalid theme instance.')

        user_theme = UserTheme.objects.create(**validated_data)
        return user_theme


def select_tasks_for_user(user):
    # Отримати список тем, які вибрав користувач
    user_themes = UserTheme.objects.filter(user=user).values_list('them', flat=True)

    tasks_to_assign = []

    # Алгоритм вибору завдань
    if len(user_themes) >= 6:
        # Розподілити завдання рівномірно між всіма темами
        for theme in user_themes:
            tasks = Task.objects.filter(theme=theme).order_by('point')
            tasks_to_assign.extend(select_tasks_by_points(tasks))
    else:
        # Вибрати додаткові завдання з перших тем
        extra_tasks_needed = 6 - len(user_themes)
        for i, theme in enumerate(user_themes):
            tasks = Task.objects.filter(theme=theme).order_by('point')
            if i < extra_tasks_needed:
                tasks_to_assign.extend(select_tasks_by_points(tasks, extra=True))
            else:
                tasks_to_assign.extend(select_tasks_by_points(tasks))

    return tasks_to_assign


def select_tasks_by_points(tasks, extra=False):
    # Розподіл за балами: 1 бал - 2 завдання, 2 бали - 2 завдання, 3 бали - 1 завдання
    tasks_by_points = {1: 2, 2: 2, 3: 1}
    selected_tasks = []

    for point, count in tasks_by_points.items():
        filtered_tasks = tasks.filter(point=point)
        count = count + 1 if extra and point == 1 else count
        selected_tasks.extend(sample(list(filtered_tasks), min(count, len(filtered_tasks))))

    return selected_tasks
