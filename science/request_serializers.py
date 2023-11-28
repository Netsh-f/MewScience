"""
============================
# @Time    : 2023/11/28 19:18
# @Author  : Elaikona
# @FileName: request_serializers.py
===========================
"""
from rest_framework import serializers


class SearchWorksSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=256)
