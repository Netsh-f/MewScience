from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view

from account.request_serializers import RegisterSerializer, LoginSerializer
from utils.decorators import validate_request
from utils.error_code import ErrorCode
from utils.response_util import api_response
from django.contrib.auth.models import User


@api_view(['POST'])
@validate_request(RegisterSerializer)
def register(request, serializer):
    if User.objects.filter(username=serializer.validated_data.get('username')):
        return api_response(ErrorCode.USERNAME_ALREADY_EXISTS)
    serializer.create(serializer.validated_data)
    return api_response(ErrorCode.SUCCESS)


@api_view(['POST'])
@validate_request(LoginSerializer)
def login_view(request, serializer):
    user = authenticate(request, **serializer.validated_data)
    if user is not None:
        login(request, user)
        return api_response(ErrorCode.SUCCESS)
    return api_response(ErrorCode.FAILED.WRONG_USERNAME_OR_PASSWORD)


@api_view(['GET'])
def logout_view(request):
    logout(request)
    return api_response(ErrorCode.SUCCESS)
