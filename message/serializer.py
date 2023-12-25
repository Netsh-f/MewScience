# ------- Litang Save The World! -------
#
# @Time    : 2023/12/22 11:14
# @Author  : Lynx
# @File    : serializer.py
#
from rest_framework import serializers

from message.models import Message


class MessageSerializer(serializers.ModelSerializer):
    timestamp = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    research_id = serializers.SerializerMethodField()
    msg_type = serializers.SerializerMethodField()
    work_type = serializers.SerializerMethodField()

    def get_research_id(self, instance: Message):
        if instance.research_id == -1: return "passed"
        elif instance.research_id == -2: return "failed"
        else: return instance.research_id

    def get_msg_type(self, instance: Message):
        return instance.MsgType(instance.msg_type).label

    def get_work_type(self, instance: Message):
        if instance.work_type == None: return "not a work transfer message"
        return instance.WorkType(instance.work_type).label

    class Meta:
        model = Message
        fields = ['research_id', 'timestamp', 'link_content', 'link_id', 'msg_type', 'work_type']