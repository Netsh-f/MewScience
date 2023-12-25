from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from MewScience import settings
from account.models import UserProfile
from account.request_serializers import RegisterSerializer, LoginSerializer, GetInfoSerializer, CollectWorkSerializer
from science.request_serializers import IdSerializer
from science.views.works import get_work_from_es_or_openalex
from utils.decorators import validate_request
from utils.error_code import ErrorCode
from utils.login_check import login_required
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
@login_required
def get_self_info_view(request):
    user = request.user
    return api_response(ErrorCode.SUCCESS, data=get_info(user))


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
        profile.identity = 1
        profile.save()
        return api_response(ErrorCode.SUCCESS)
    else:
        return api_response(ErrorCode.NOT_LOGGED_IN)


def get_info(user):
    return GetInfoSerializer(user).data


@api_view(['PUT'])
@login_required
def update_self_intro(request):
    profile = UserProfile.objects.get(user=request.user)
    intro = request.data.get('intro')
    profile.intro = intro
    profile.save()
    return api_response(ErrorCode.SUCCESS)


# 获取关注列表
@api_view(['GET'])
@login_required
def get_follow_list(request):
    profile = UserProfile.objects.get(user=request.user)
    return api_response(ErrorCode.SUCCESS, profile.follow_list)


@api_view(['POST'])
@login_required
@validate_request(CollectWorkSerializer)
def collect_work(request, serializer):
    work_id = serializer.validated_data.get('work_id')
    work = get_work_from_es_or_openalex(work_id)
    profile = UserProfile.objects.get(user=request.user)

    if work is not None:
        author_list = []
        for authorship in work.get('authorships'):
            author_list.append(authorship.get('author'))
        profile.collect_list[work_id] = {
            "title": work.get('title'),
            "authorships": author_list,
        }
        profile.save()
    return api_response(ErrorCode.SUCCESS)


@api_view(['GET'])
@login_required
def get_collect_list(request):
    profile = UserProfile.objects.get(user=request.user)
    return api_response(ErrorCode.SUCCESS, profile.collect_list)


@api_view(['POST'])
@login_required
@validate_request(CollectWorkSerializer)
def cancel_collect_work(request, serializer):
    work_id = serializer.validated_data.get('work_id')
    profile = UserProfile.objects.get(user=request.user)
    if str(work_id) in profile.collect_list:
        del profile.collect_list[str(work_id)]
        print(profile.collect_list)
        profile.save()
        return api_response(ErrorCode.SUCCESS)
    return api_response(ErrorCode.WORK_NOT_FOUND)


@api_view(['GET'])
@login_required
@validate_request(CollectWorkSerializer)
def is_work_collected(request, serializer):
    work_id = serializer.validated_data.get('work_id')
    result = {}
    if request.user.is_authenticated and str(work_id) in request.user.userprofile.collect_list:
        result['collected'] = True
    else:
        result['collected'] = False
    return api_response(ErrorCode.SUCCESS, result)
