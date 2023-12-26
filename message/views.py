from django.shortcuts import render
from rest_framework.decorators import api_view

from message.models import Message
from message.serializer import MessageSerializer
from utils.error_code import ErrorCode
from utils.login_check import login_required
from utils.response_util import api_response


# Create your views here.

@api_view(['GET'])
def get_msg_list(request):
    if request.user.is_authenticated:
        messages = Message.objects.filter(user=request.user)
        return api_response(ErrorCode.SUCCESS, data=MessageSerializer(messages, many=True).data)
    else:
        return api_response(ErrorCode.NOT_LOGGED_IN)

@api_view(['PUT'])
@login_required
def update_message_status(request):
    id = request.data.get('id')
    message = Message.objects.filter(id=id).first()
    if message is None:
        return api_response(ErrorCode.MSG_NOT_FOUND)
    else:
        message.status = True
        message.save()
        return api_response(ErrorCode.SUCCESS)