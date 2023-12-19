"""
============================
# @Time    : 2023/11/6 16:12
# @Author  : Elaikona
# @FileName: request_serializers.py
===========================
"""
from rest_framework import serializers
from django.contrib.auth.models import User

from account.models import UserProfile


class RegisterSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user, identity=UserProfile.Identify.NORMAL, researcher_id=None)
        return user

    username = serializers.CharField(max_length=128)
    password = serializers.CharField(max_length=128)
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=128)
    last_name = serializers.CharField(max_length=128)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=128)
    password = serializers.CharField(max_length=128)


class GetSomethingSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=128)
