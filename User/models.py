from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    image_url = models.CharField(max_length=255, default='None')
    score = models.IntegerField(default=0)
    count_tasks = models.IntegerField(default=0)

    REQUIRED_FIELDS = ('email', 'first_name', 'last_name', 'password')

    class Meta:
        db_table = "user"