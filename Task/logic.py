from Task.models import *
from random import sample


from random import sample

def select_user_tasks(username):
    user_themes = UserTheme.objects.filter(user_id=username).values_list('theme_id', flat=True)
    tasks_to_assign = []
    used_themes = set()  # Для зберігання тем, з яких вже вибрано завдання

    if len(user_themes) == 6:
        tasks_by_points = {1: 2, 2: 2, 3: 1}

        for point, count in tasks_by_points.items():
            for _ in range(count):
                for theme in user_themes:
                    if theme not in used_themes:
                        tasks = Task.objects.filter(theme_id=theme, point=point).order_by('point')

                        if tasks:
                            task = sample(list(tasks), 1)[0]
                            tasks_to_assign.append(task)
                            used_themes.add(theme)
                            break

                # Перевірка, чи достатньо завдань для вибору
                if len(used_themes) == len(user_themes):
                    break

    task_names = [task.name for task in tasks_to_assign]
    return task_names


def create_tasklist(username):
    task_ids = select_user_tasks(username)
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
