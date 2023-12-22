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


class SearchAuthorsSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=128)
    institution = serializers.CharField(max_length=128, allow_null=True)
    page = serializers.IntegerField(allow_null=True)
    page_size = serializers.IntegerField(allow_null=True)


class GetInstitutionSerializer(serializers.Serializer):
    id = serializers.IntegerField()


class GetResearcherSerializer(serializers.Serializer):
    id = serializers.IntegerField()
