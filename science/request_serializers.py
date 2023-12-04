"""
============================
# @Time    : 2023/11/28 19:18
# @Author  : Elaikona
# @FileName: request_serializers.py
===========================
"""
from rest_framework import serializers


class SearchWorksSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=256, allow_null=True)
    author = serializers.CharField(max_length=128, allow_null=True)
    source = serializers.CharField(max_length=128, allow_null=True)
    start_year = serializers.IntegerField(allow_null=True)
    end_year = serializers.IntegerField(allow_null=True)
