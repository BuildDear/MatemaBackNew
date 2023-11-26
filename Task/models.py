from django.db import models
from django.contrib.auth.models import User

from Matema import settings


class TypeAnswer(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        db_table = "TypeAnswer"


class Theme(models.Model):
    name = models.CharField(max_length=30, primary_key=True)

    class Meta:
        db_table = "Theme"


class Task(models.Model):
    name = models.CharField(max_length=100, unique=True, primary_key=True)
    text = models.TextField()
    image_url = models.CharField(max_length=255)
    point = models.IntegerField()
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, to_field='name')
    type_ans = models.ForeignKey(TypeAnswer, on_delete=models.CASCADE)
    answer = models.TextField()

    class Meta:
        db_table = "Task"


class TaskList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, to_field='username')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, to_field='name')
    is_weekly = models.BooleanField()

    class Meta:
        db_table = "TaskList"


class UserTheme(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, to_field='username')
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, to_field='name')

    class Meta:
        db_table = "UserTheme"


class DoneTask(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, to_field='username')
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, to_field='name')
    is_done = models.BooleanField()

    class Meta:
        db_table = "DoneTask"
