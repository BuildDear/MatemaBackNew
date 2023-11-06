from django.db import models
from Task.models import *
from User.models import *


class TaskList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    is_current = models.BooleanField()
    is_done = models.BooleanField()
    is_weekly = models.BooleanField()
    point = models.IntegerField(null=True)

    class Meta:
        db_table = "TaskList"


class UserThem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    them = models.ForeignKey(Them, on_delete=models.CASCADE)

    class Meta:
        db_table = "user_them"

