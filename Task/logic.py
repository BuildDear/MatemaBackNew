from Task.models import *
from random import sample


def select_user_tasks(username, extra=False):
    user_themes = UserTheme.objects.filter(user_id=username).values_list('theme_id', flat=True)
    print(user_themes)
    tasks_to_assign = []

    # Перевірка, що є рівно 6 різних тем
    if len(user_themes) == 6:
        # Розподіл балів для завдань
        tasks_by_points = {1: 2, 2: 2, 3: 1}

        # Перебираємо теми та вибираємо завдання
        for theme in user_themes:
            tasks = Task.objects.filter(theme_id=theme).order_by('point')
            print(tasks)

            # Вибираємо завдання згідно з розподілом балів
            for point, count in tasks_by_points.items():
                filtered_tasks = tasks.filter(point=point)

                # Додаткова перевірка на випадок, якщо фільтрованих завдань менше, ніж потрібно
                count = min(count, len(filtered_tasks))

                if count > 0:
                    selected_tasks = sample(list(filtered_tasks), count)
                    tasks_to_assign.extend(selected_tasks)

                    # Видаляємо вибрані завдання з розподілу
                    tasks_by_points[point] -= len(selected_tasks)

    # Отримуємо назви завдань
    task_names = [task.name for task in tasks_to_assign]
    return task_names


def create_tasklist(username):
    # user = settings.AUTH_USER_MODEL.objects.get(username=username)
    task_ids = select_user_tasks(username)
    print("=====")
    print(task_ids)
    tasklists = []


    for task_id in task_ids:
        task = Task.objects.get(name=task_id)
        tasklist = TaskList.objects.create(
            user=username,
            task=task,
            is_current=False,
            is_done=False,
            is_weekly=False,
            point=0
        )
        tasklists.append(tasklist)

    return tasklists


"""
class GenerateUserTasksView(APIView):
 
    Клас відображення для отримання завдань для користувача.
 
    def get(self, request, *args, **kwargs):
        # Перевірка, що користувач авторизований
        user = request.user
        if user.is_authenticated:
            # Вибір завдань для користувача
            tasks = select_tasks_for_user(user)
            # Серіалізація завдань та відправлення відповіді
            tasks_data = [{'name': task.name, 'points': task.point} for task in tasks]
            return Response({'tasks': tasks_data})
        else:
            return Response({'error': 'Користувач не авторизований'}, status=401)
"""
