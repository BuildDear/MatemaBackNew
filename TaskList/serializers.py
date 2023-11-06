from rest_framework import serializers
from .models import *
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from djoser.serializers import UserCreateSerializer


class TaskListCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = "__all__"


class TaskListDeleteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = "__all__"


class TaskListGenerateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = "__all__"

