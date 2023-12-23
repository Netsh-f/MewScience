from rest_framework import serializers


class ProjectSerializer(serializers.Serializer):
    author_id = serializers.CharField(max_length=16)