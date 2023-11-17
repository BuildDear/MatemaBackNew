from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRole(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        db_table = "user_role"


class User(AbstractUser):
    image_url = models.CharField(max_length=255, default='None')
    score = models.IntegerField(default=0)
    count_tasks = models.IntegerField(default=0)
    role = models.ForeignKey(UserRole, on_delete=models.SET_NULL, default=1, null=True)

    REQUIRED_FIELDS = ('email', 'first_name', 'last_name', 'password')

    class Meta:
        db_table = "user"
