from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from datetime import datetime
from Task.models import Task

# Creating a scheduler object
scheduler = BackgroundScheduler()

# Adding a job store for DjangoJobStore jobs and assigning it the name "default"
scheduler.add_jobstore(DjangoJobStore(), "default")

# Decorator for registering a job that will be executed daily at the specified hour
@register_job(scheduler, "cron", hour='0', minute='1', replace_existing=True)# Change only the time here
def change_task_list():
    today = datetime.today()

    # Determining if the current day is even
    is_even_day = today.day % 2 == 0
    # Getting all tasks with odd IDs
    all_tasks = list(Task.objects.all())

    if is_even_day:
        # Getting all tasks with even IDs
        even_id_tasks = [task for task in all_tasks if all_tasks.index(task) % 2 == 0]

        # Printing information about tasks with even IDs
        for task in even_id_tasks:
            print(f"Task Name: {task.name}")
            print(f"Task ID: {all_tasks.index(task)}")
            print("------------")
    else:
        odd_id_tasks = [task for task in all_tasks if all_tasks.index(task) % 2 != 0]

        # Printing information about tasks with odd IDs
        for task in odd_id_tasks:
            print(f"Task Name: {task.name}")
            print(f"Task ID: {all_tasks.index(task)}")
            print("------------")

# Registering events and starting the scheduler
register_events(scheduler)
scheduler.start()
