from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view

from account.models import UserProfile
from account.request_serializers import RegisterSerializer, LoginSerializer, GetInfoSerializer
from utils.decorators import validate_request
from utils.error_code import ErrorCode
from utils.response_util import api_response
from django.contrib.auth.models import User


@api_view(['POST'])
@validate_request(RegisterSerializer)
def register(request, serializer):
    if User.objects.filter(username=serializer.validated_data.get('username')):
        return api_response(ErrorCode.USERNAME_ALREADY_EXISTS)
    user = serializer.create(serializer.validated_data)
    UserProfile.objects.create(user=user)
    return api_response(ErrorCode.SUCCESS)


@api_view(['POST'])
@validate_request(LoginSerializer)
def login_view(request, serializer):
    user: User = authenticate(request, **serializer.validated_data)
    data = {
        'identify': UserProfile.objects.get(user=user).identity
    }

    if user is not None:
        login(request, user)
        return api_response(ErrorCode.SUCCESS, data)
    return api_response(ErrorCode.WRONG_USERNAME_OR_PASSWORD)


@api_view(['GET'])
def logout_view(request):
    logout(request)
    return api_response(ErrorCode.SUCCESS)


@api_view(['POST'])
def get_info_view(request):
    if request.user.is_authenticated:
        user = request.user
        return api_response(ErrorCode.SUCCESS, data=GetInfoSerializer(user).data)
    else:
        return api_response(ErrorCode.NOT_LOGGED_IN)

