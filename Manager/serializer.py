from rest_framework import serializers
from django.core.exceptions import ValidationError
from Task.models import Task, Theme, TypeAnswer

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
        if Task.objects.filter(name=validated_data['name']).exists():
            raise serializers.ValidationError('A task with that name already exists.')

        theme = validated_data.get('theme')
        if not isinstance(theme, Theme):
            raise serializers.ValidationError('Invalid ID for theme.')

        type_ans = validated_data.get('type_ans')
        if not isinstance(type_ans, TypeAnswer):
            raise serializers.ValidationError('Invalid ID for type_ans.')

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


class TaskAnswerSerializer(serializers.Serializer):
    answer_data = serializers.JSONField()

    def validate(self, data):
        answer_data = data['answer_data']

        # Check if the provided JSON data is valid
        if not isinstance(answer_data, dict):
            raise serializers.ValidationError("Invalid answer data format")

        return data

class TaskPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['photo']


class TaskTypeSetSerializer(serializers.Serializer):
    type_ans = serializers.CharField(max_length=50)

    def validate_type_ans(self, value):
        try:
            # Try to get the TypeAnswer instance based on the provided type
            type_ans_instance = TypeAnswer.objects.get(name=value)
            return type_ans_instance
        except TypeAnswer.DoesNotExist:
            raise serializers.ValidationError("Invalid type_ans value.")

class TypeAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeAnswer
        fields = ['name']