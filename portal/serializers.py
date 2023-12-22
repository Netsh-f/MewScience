# ------- Litang Save The World! -------
#
# @Time    : 2023/12/19 20:51
# @Author  : Lynx
# @File    : serializers.py
#
from rest_framework import serializers

from portal.models import Application


class ClaimPortalSerializer(serializers.Serializer):
    research_id = serializers.IntegerField


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['id', 'user', 'research_id', 'research_name', 'create_time']