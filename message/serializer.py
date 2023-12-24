# ------- Litang Save The World! -------
#
# @Time    : 2023/12/22 11:14
# @Author  : Lynx
# @File    : serializer.py
#
from rest_framework import serializers

from message.models import Message


class MessageSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()
    timestamp = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    def get_content(self, instance:Message):
        if instance.research_id == -1:
            return f"您对学者门户{instance.link_content}的认领申请已通过！"
        elif instance.research_id == -2:
            return f"您对学者门户{instance.link_content}的认领申请未通过，请联系管理员获取详细信息！"
        else:
            return f"您关注的学者产出了新的学术成果：{instance.link_content}"
    class Meta:
        model = Message
        fields = ['research_id', 'content', 'timestamp', 'link_content', 'link_id']