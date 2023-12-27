import random
from Task.models import *
from celery import shared_task

from django.contrib.auth import get_user_model


User = get_user_model()


@shared_task
def select_user_tasks(username):
    user_themes = list(UserTheme.objects.filter(user_id=username).values_list('theme', flat=True))

    tasks_to_assign = []
    used_themes = set()  # Для зберігання тем, з яких вже вибрано завдання

    tasks_by_points = {1: 2, 2: 2, 3: 1}
    total_required_tasks = sum(tasks_by_points.values())  # Загальна кількість необхідних завдань

    # Перша спроба вибрати завдання з унікальних тем
    for point, count in tasks_by_points.items():
        for _ in range(count):
            for theme_id in user_themes:
                if theme_id not in used_themes:
                    tasks = Task.objects.filter(theme=theme_id, point=point).order_by('point')
                    if tasks:
                        task = random.choice(list(tasks))
                        tasks_to_assign.append(task)
                        used_themes.add(theme_id)
                        break

    # Якщо не вистачає завдань, повторно перебираємо теми
    if len(tasks_to_assign) < total_required_tasks:
        additional_themes = user_themes * ((total_required_tasks - len(tasks_to_assign)) // len(user_themes) + 1)
        for point, count in tasks_by_points.items():
            for _ in range(count - len([task for task in tasks_to_assign if task.point == point])):
                for theme_id in additional_themes:
                    if theme_id not in used_themes or len(used_themes) == len(user_themes):
                        tasks = Task.objects.filter(theme=theme_id, point=point).exclude(
                            id__in=[task.id for task in tasks_to_assign]).order_by('point')
                        if tasks:
                            task = random.choice(list(tasks))
                            tasks_to_assign.append(task)
                            used_themes.add(theme_id)
                            break

                if len(tasks_to_assign) >= total_required_tasks:
                    break

    task_names = [task.name for task in tasks_to_assign]
    return task_names


@shared_task
def create_tasklist(username):
    user = User.objects.get(username=username)

    task_names = select_user_tasks.delay(username)

    task_names = task_names.get()

    tasklists = []
    for task_name in task_names:
        task = Task.objects.get(name=task_name)
        tasklist, created = TaskList.objects.get_or_create(
            user=user,
            task=task,
            defaults={'is_weekly': False},
        )
        tasklists.append(tasklist)

    return [tasklist.id for tasklist in tasklists]
