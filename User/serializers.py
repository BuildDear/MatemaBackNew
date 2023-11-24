from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from rest_framework import serializers
from .models import User
from djoser.serializers import UserCreateSerializer


class CustomUserCreateSerializer(UserCreateSerializer):
    """Registration user"""
    re_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password", "re_password")
        extra_kwargs = {"password": {"write_only": True, "required": True, "validators": [validate_password]}, }

    def validate(self, attrs):
        if attrs["password"] != attrs["re_password"]:
            raise serializers.ValidationError({"re_password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        with transaction.atomic():
            user = User.objects.create(
                username=validated_data["username"],
                email=validated_data["email"],
                first_name=validated_data["first_name"],
                last_name=validated_data["last_name"]
            )
            user.set_password(validated_data["password"])
            user.save()
            return user


class UserPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['photo']
        # Add this line if the photo field allows null values
        extra_kwargs = {'photo': {'allow_null': True}}
