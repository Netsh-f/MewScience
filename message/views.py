from django.shortcuts import render
from rest_framework.decorators import api_view

from message.models import Message
from message.serializer import MessageSerializer
from utils.error_code import ErrorCode
from utils.response_util import api_response


# Create your views here.

@api_view(['GET'])
def get_msg_list(request):
    if request.user.is_authenticated:
        messages = Message.objects.filter(user=request.user)
        return api_response(ErrorCode.SUCCESS, data=MessageSerializer(messages, many=True).data)
    else:
        return api_response(ErrorCode.NOT_LOGGED_IN)