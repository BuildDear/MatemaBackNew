from django.db import models
from Task.models import *


class UserRole(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        db_table = "user_role"


class User(models.Model):
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
