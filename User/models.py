from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRole(models.Model):
    name = models.CharField(max_length=30, default=0)

    class Meta:
        db_table = "user_role"


class User(AbstractUser):
    image_url = models.CharField(max_length=255, default=None)
    score = models.IntegerField(default=0)
    count_tasks = models.IntegerField(default=0)
    role = models.ForeignKey(UserRole, on_delete=models.SET_NULL, default=1, null=True)

    class Meta:
        db_table = "user"
