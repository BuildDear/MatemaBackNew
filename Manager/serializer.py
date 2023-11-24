from rest_framework import serializers
from django.core.exceptions import ValidationError
from Task.models import *
from User.models import User


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = "__all__"


class ThemeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Theme
        fields = "__all__"


class TypeAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = TypeAnswer
        fields = "__all__"


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"

    def create(self, validated_data):
        theme = validated_data.get('theme')
        if not isinstance(theme, Theme):
            raise serializers.ValidationError('Invalid theme instance.')

        # Перевірка type_ans
        type_ans = validated_data.get('type_ans')
        if not isinstance(type_ans, TypeAnswer):
            raise serializers.ValidationError('Invalid type_ans instance.')

        task = Task.objects.create(**validated_data)
        return task


class ThemeCreateSerializer(serializers.ModelSerializer):

    def create_theme(self, name):
        if Theme.objects.filter(id=name).exists():
            raise ValidationError('A theme with that name already exists.')

        theme = Theme.objects.create(name=name)
        return theme

    class Meta:
        model = Theme
        fields = "__all__"


class UserListSerializer(serializers.ModelSerializer):
    """List of users"""

    class Meta:
        model = User
        fields = "__all__"


class UserDetailSerializer(serializers.ModelSerializer):
    """All user"""

    class Meta:
        model = User
        fields = "__all__"


class TypeAnswerCreateSerializer(serializers.ModelSerializer):

    def create_type_answer(self, name):
        if TypeAnswer.objects.filter(id=name).exists():
            raise ValidationError('A TypeAnswer with that name already exists.')

        type_ans = TypeAnswer.objects.create(name=name)
        return type_ans

    class Meta:
        model = TypeAnswer
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


class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskList
        fields = "__all__"

