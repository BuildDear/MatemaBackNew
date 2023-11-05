from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRole(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        db_table = "user_role"


class User(AbstractUser):
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=254)
    image_url = models.CharField(max_length=255)
    password = models.CharField(max_length=128)
    score = models.IntegerField()
    count_tasks = models.IntegerField()
    role = models.ForeignKey(UserRole, on_delete=models.CASCADE)
    is_active = models.BooleanField()
    is_superuser = models.BooleanField()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = "user"


class TypeAnswer(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        db_table = "type_answer"


class Them(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        db_table = "them"


class Task(models.Model):
    name = models.CharField(max_length=100, unique=True)
    text = models.TextField()
    image_url = models.CharField(max_length=255)
    point = models.IntegerField()
    them = models.ForeignKey(Them, on_delete=models.CASCADE)
    type = models.ForeignKey(TypeAnswer, on_delete=models.CASCADE)
    answer = models.TextField()

    class Meta:
        db_table = "task"


class TaskList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    is_current = models.BooleanField()
    is_done = models.BooleanField()
    is_weekly = models.BooleanField()
    point = models.IntegerField(null=True)

    class Meta:
        db_table = "task_list"


class UserThem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    them = models.ForeignKey(Them, on_delete=models.CASCADE)

    class Meta:
        db_table = "user_them"
