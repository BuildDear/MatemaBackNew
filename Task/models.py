from django.db import models
from django.core.exceptions import ValidationError, ObjectDoesNotExist


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
        db_table = "Task"
