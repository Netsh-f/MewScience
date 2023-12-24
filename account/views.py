from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from MewScience import settings
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


@api_view(['GET'])
def get_self_info_view(request):
    if request.user.is_authenticated:
        user = request.user
        return api_response(ErrorCode.SUCCESS, data=get_info(user))
    else:
        return api_response(ErrorCode.NOT_LOGGED_IN)

@api_view(['GET'])
def get_info_view(request):
    user_id = request.GET.get('user_id')
    if user_id is None:
        return api_response(ErrorCode.INVALID_DATA)

    user = User.objects.filter(id=user_id).first()
    if user is None:
        return api_response(ErrorCode.USER_NOT_EXIST)

    return api_response(ErrorCode.SUCCESS, data=get_info(user))

@api_view(['PUT'])
def set_admin_view(request):
    if not settings.DEBUG:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.user.is_authenticated:
        user = request.user
        profile = UserProfile.objects.get(user=user)
        profile.identity=1
        profile.save()
        return api_response(ErrorCode.SUCCESS)
    else:
        return api_response(ErrorCode.NOT_LOGGED_IN)

def get_info(user):
    return GetInfoSerializer(user).data

@api_view(['PUT'])
def update_self_intro(request):
    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        intro = request.data.get('intro')
        profile.intro = intro
        profile.save()
        return api_response(ErrorCode.SUCCESS)
    else:
        return api_response(ErrorCode.NOT_LOGGED_IN)

# 获取关注列表
@api_view(['GET'])
def get_follow_list(request):
    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        return api_response(ErrorCode.SUCCESS, profile.follow_list)
    else:
        return api_response(ErrorCode.NOT_LOGGED_IN)