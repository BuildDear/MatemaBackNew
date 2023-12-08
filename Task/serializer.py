from Task.models import *
from django.contrib.auth import get_user_model
from rest_framework import serializers
import random
User = get_user_model()


def select_user_tasks(username):
    user_themes = list(UserTheme.objects.filter(user_id=username).values_list('theme_id', flat=True))
    random.shuffle(user_themes)  # Перемішування списку тем
    tasks_to_assign = []
    used_themes = set()  # Для зберігання тем, з яких вже вибрано завдання
    used_tasks = set()   # Для зберігання ID завдань, щоб уникнути дублікації

    tasks_by_points = {1: 2, 2: 2, 3: 1}
    total_required_tasks = sum(tasks_by_points.values())  # Загальна кількість необхідних завдань

    for point, count in tasks_by_points.items():
        for _ in range(count):
            for theme_id in user_themes:
                tasks = Task.objects.filter(theme_id=theme_id, point=point).exclude(id__in=used_tasks).order_by('point')
                if tasks:
                    task = random.choice(list(tasks))
                    tasks_to_assign.append(task)
                    used_tasks.add(task.id)  # Зберігаємо ID завдання, щоб уникнути повторного використання
                    used_themes.add(theme_id)
                    break

            if len(used_themes) == len(user_themes):
                break

    if len(tasks_to_assign) < total_required_tasks:
        print("Not enough tasks to generate TaskList.")

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
    class Meta:
        model = TaskList
        fields = "__all__"


class DoneTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoneTask
        fields = ['user', 'task', 'is_done', 'datetime']


''' 
class DoneTaskSerializer(serializers.ModelSerializer):
    task_details = TaskSerializer(source='task', read_only=True)  # 'task' відповідає назві ForeignKey поля в моделі DoneTask

    class Meta:
        model = DoneTask
        fields = ['user', 'task', 'is_done', 'datetime', 'task_details']
'''