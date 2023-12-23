"""
============================
# @Time    : 2023/11/28 19:18
# @Author  : Elaikona
# @FileName: request_serializers.py
===========================
"""
from rest_framework import serializers


class SearchWorksSerializer(serializers.Serializer):
    query = serializers.CharField(max_length=256)
    page = serializers.IntegerField(allow_null=True)
    page_size = serializers.IntegerField(allow_null=True)
    min_score = serializers.IntegerField(allow_null=True)
    sort = serializers.CharField(max_length=32, allow_null=True)
    order = serializers.CharField(max_length=8, allow_null=True)


class AdvancedSearchWorksSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=256, allow_null=True)
    # doi = serializers.URLField(allow_null=True)
    # publication_year = serializers.DateField(allow_null=True)
    # language = serializers.CharField(max_length=2, allow_null=True)
    # type = serializers.CharField(max_length=16, allow_null=True)
    # is_oa = serializers.CharField(max_length=5, allow_null=True)
    author = serializers.CharField(max_length=128, allow_null=True)


class GetHotSerializer(serializers.Serializer):
    index = serializers.CharField(max_length=32)
    sort = serializers.CharField(max_length=32, allow_null=True)


class SearchAuthorsSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=128)
    institution = serializers.CharField(max_length=128, allow_null=True)
    page = serializers.IntegerField(allow_null=True)
    page_size = serializers.IntegerField(allow_null=True)


class IdSerializer(serializers.Serializer):
    id = serializers.IntegerField()
