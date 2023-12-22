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

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['research_id']

class GetInfoSerializer(serializers.ModelSerializer):
    research_id = serializers.SerializerMethodField()
    class Meta:
        model = User
        field = ['username', 'password', 'email', 'first_name', 'last_name']

    def get_research_id(self, obj):
        try:
            profile = UserProfile.objects.get(user=obj)
            return profile.researcher_id
        except UserProfile.DoesNotExist:
            return None
