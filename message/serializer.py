# ------- Litang Save The World! -------
#
# @Time    : 2023/12/22 11:14
# @Author  : Lynx
# @File    : serializer.py
#
from rest_framework import serializers

from message.models import Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        field = ['research_id', 'content', 'timestamp']