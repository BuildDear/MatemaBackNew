from Task.models import *
from django.contrib.auth import get_user_model
from rest_framework import serializers
import random

from random import sample
from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()


def select_user_tasks(username):
    user_themes = list(UserTheme.objects.filter(user_id=username).values_list('theme_id', flat=True))
    
    random.shuffle(user_themes)  # Перемішування списку тем

    print(user_themes)
    random.shuffle(user_themes)  # Перемішування списку тем
    tasks_to_assign = []
    used_themes = set()  # Для зберігання тем, з яких вже вибрано завдання

    tasks_by_points = {1: 2, 2: 2, 3: 1}
    total_required_tasks = sum(tasks_by_points.values())  # Загальна кількість необхідних завдань

    for point, count in tasks_by_points.items():
        for _ in range(count):
            for theme_id in user_themes:
                if theme_id not in used_themes:
                    tasks = Task.objects.filter(theme_id=theme_id, point=point).order_by('point')
                    if tasks:
                        task = random.choice(list(tasks))
                        tasks_to_assign.append(task)
                        used_themes.add(theme_id)
                        break

            if len(used_themes) == len(user_themes):
                break

    if len(tasks_to_assign) < total_required_tasks:
        print("Not enough tasks to generate TaskList.")
    user_themes = UserTheme.objects.filter(user_id=username).values_list('theme_id', flat=True)

    task_names = [task.name for task in tasks_to_assign]
    return task_names


def create_tasklist(username):
    user = User.objects.get(username=username)
    task_name = select_user_tasks(username)
    tasklists = []

    for task_id in task_name:
        task = Task.objects.get(name=task_id)
        tasklist = TaskList.objects.create(
            user=user,
            task=task,
            is_weekly=False,
        )
        tasklists.append(tasklist)

    return tasklists


class TaskListSerializer(serializers.ModelSerializer):
    theme_name = serializers.CharField(source='task.theme.name', read_only=True)
    class Meta:
        model = DoneTask
        fields = ['id', 'datetime', 'task_id', 'user_id', 'theme_name']

    class Meta:
        model = TaskList
        fields = "__all__"
        

class DoneTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoneTask
        fields = ['user', 'task', 'is_done', 'datetime']


class TypeAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeAnswer
        fields = ['name']

        
class TaskSerializer(serializers.ModelSerializer):
    type_ans = TypeAnswerSerializer()

    class Meta:
        model = Task
        fields = ['id', 'name', 'text', 'point', 'photo', 'answer_matching', 'answer_short', 'answer_mcq', 'theme', 'type_ans']

        
class UserThemeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTheme
        fields = "__all__"

    def create(self, validated_data):
        theme = validated_data.get('theme')
        if not isinstance(theme, Theme):
            raise serializers.ValidationError('Invalid theme instance.')

        user = validated_data.get('user')
        if not isinstance(user, User):
            raise serializers.ValidationError('Invalid user instance.')

        user_theme = UserTheme.objects.create(**validated_data)
        return user_theme


class UserNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = ['username']



