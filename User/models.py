from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=30, unique=True, default="")
    first_name = models.CharField(max_length=30, blank=True, default="")
    last_name = models.CharField(max_length=30, blank=True, default="")
    email = models.EmailField(blank=True, max_length=254, unique=True)
    point = models.BigIntegerField(default=0)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    class Meta:
        db_table = "user"
