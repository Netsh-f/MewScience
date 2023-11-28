"""
============================
# @Time    : 2023/11/28 19:49
# @Author  : Elaikona
# @FileName: serializers.py
===========================
"""
from rest_framework import serializers

from science.models import Works


class WorksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Works
        exclude = ['id']
