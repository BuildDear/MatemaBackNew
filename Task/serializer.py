from Task.models import *
import random

from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class TaskForListSerializer(serializers.ModelSerializer):
    theme = serializers.CharField(source='theme.name')

    class Meta:
        model = Task
        fields = ['id', 'name', 'point', 'theme']


class TaskListSerializer(serializers.ModelSerializer):
    task = TaskForListSerializer(read_only=True)

    class Meta:
        model = TaskList
        fields = ['task', 'is_weekly']


class DoneTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoneTask
        fields = ['user', 'task', 'is_done', 'datetime', 'mark']


class TypeAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeAnswer
        fields = ['name']


class TaskSerializer(serializers.ModelSerializer):
    type_ans = TypeAnswerSerializer()

    class Meta:
        model = Task
        fields = "__all__"


class UserThemeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTheme
        fields = "__all__"

    def create(self, validated_data):
        theme = validated_data.get('theme')
        if not isinstance(theme, Theme):
            raise serializers.ValidationError('Invalid theme instance.')

        user = validated_data.get('user')
        if not isinstance(user, User):
            raise serializers.ValidationError('Invalid user instance.')

        user_theme = UserTheme.objects.create(**validated_data)
        return user_theme


class UserNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = ['username']
