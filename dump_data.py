import os
import django
from django.core.serializers import serialize

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Matema.settings')
django.setup()

from Task.models import TypeAnswer, Theme, Task, TaskList, UserTheme, DoneTask
from User.models import User


def dump_model_data(model, filename):
    data = serialize('json', model.objects.all(), ensure_ascii=False)
    with open(f'fixtures/{filename}', 'w', encoding='utf-8') as file:
        file.write(data)

# Виклик функції для кожної моделі
dump_model_data(TypeAnswer, 'typeanswer_fixture.json')
dump_model_data(Theme, 'theme_fixture.json')
dump_model_data(Task, 'task_fixture.json')
dump_model_data(TaskList, 'tasklist_fixture.json')
dump_model_data(UserTheme, 'usertheme_fixture.json')
dump_model_data(DoneTask, 'donetask_fixture.json')
dump_model_data(User, 'user_fixture.json')
