from django.db import models
from django.contrib.auth.models import User

from Matema import settings


class TypeAnswer(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        db_table = "type_answer"


class Theme(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        db_table = "theme"


class Task(models.Model):
    name = models.CharField(max_length=100, unique=True)
    text = models.TextField()
    image_url = models.CharField(max_length=255)
    point = models.IntegerField()
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)
    type_ans = models.ForeignKey(TypeAnswer, on_delete=models.CASCADE)
    answer = models.TextField()

    class Meta:
        db_table = "Task"


class TaskList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    is_current = models.BooleanField()
    is_done = models.BooleanField()
    is_weekly = models.BooleanField()
    point = models.IntegerField(null=True)

    class Meta:
        db_table = "TaskList"


class UserTheme(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    them = models.ForeignKey(Theme, on_delete=models.CASCADE)

    class Meta:
        db_table = "UserTheme"
