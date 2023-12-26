import os

from rest_framework.decorators import api_view

from MewScience import settings
from MewScience.settings import ES
from account.models import UserProfile
from message.models import Message
from portal.models import Application
from portal.serializers import ApplicationSimpleSerializer, ApplicationDetailedSerializer
from utils.error_code import ErrorCode
from utils.file_check import file_check
from utils.login_check import login_required
from utils.response_util import api_response

def get_researcher_name_by_id(researcher_id):
    result = ES.get(index='authors', id=researcher_id)
    return result.get('_source').get('display_name')


# 申请认领门户
@api_view(['POST'])
@login_required
def claim_portal(request):
    user = request.user
    profile = UserProfile.objects.get(user=user)
    if profile.researcher_id is not None:
        return api_response(ErrorCode.ALREADY_CLAIM_PORTAL)

    research_id = request.data.get('research_id')
    message = request.data.get('message')

    # tuple = { T/F, ERRNO/file}
    tuple = file_check(request.FILES.get('file'), settings.MAX_APPLICATION_FILE_SIZE)
    if not tuple[0]:
        return api_response(tuple[1])
    file = tuple[1]

    if research_id is not None and message is not None:
        # File handle
        file_ext = file.name.split('.')[-1]
        path = os.path.join(settings.APPLICATION_ROOT, f"{user.id}-{research_id}-application.{file_ext}")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            for chunk in file.chunks():
                f.write(chunk)

        file_url = os.path.join(settings.APPLICATION_URL, f"{user.id}-{research_id}-application.{file_ext}")
        research_name = get_researcher_name_by_id(research_id)

        if research_name is None:
            return api_response(ErrorCode.ELASTIC_ERROR)

        if Application.objects.filter(user=user, research_id=research_id).exists():
            application = Application.objects.filter(user=user, research_id=research_id).first()
            application.message = message
            application.file = file_url
            application.save()
        else:
            Application.objects.create(user=user,
                                       research_id=research_id,
                                       research_name=research_name,
                                       message=message,
                                       file=file_url)
        return api_response(ErrorCode.SUCCESS)
    else:
        return api_response(ErrorCode.INVALID_DATA)


# 获取门户对应用户
def get_user_by_portal(research_id) -> dict:
    if research_id is None:
        return {}
    profile = UserProfile.objects.filter(researcher_id=research_id).first()
    if profile is None:
        return {'claim_info': {'has_been_claimed': False}}
    else:
        return {'claim_info': {
            'has_been_claimed': True,
            'user_id': profile.user_id,
            'user_name': profile.user.username,
            'user_intro': profile.intro,
        }}


# 关注指定门户
@api_view(['PUT'])
@login_required
def follow_portal(request):
    user = request.user
    research_id = request.data.get('research_id')
    research_name = get_researcher_name_by_id(research_id)
    if research_id is None or research_name is None:
        return api_response(ErrorCode.INVALID_DATA)
    else:
        profile = UserProfile.objects.get(user=user)
        if profile.follow_list.get(research_id) is not None:
            return api_response(ErrorCode.ALREADY_FOLLOWED)
        profile.follow_list[research_id] = research_name
        profile.save()
    return api_response(ErrorCode.SUCCESS)


# 取消关注门户
@api_view(['PUT'])
@login_required
def unfollow_portal(request):
    research_id = request.data.get('research_id')
    if research_id is None:
        return api_response(ErrorCode.INVALID_DATA)
    profile = UserProfile.objects.get(user=request.user)
    if research_id in profile.follow_list:
        del profile.follow_list[research_id]
        profile.save()
    return api_response(ErrorCode.SUCCESS)


# 获取申请列表
@api_view(['GET'])
@login_required
def get_applications_list(request):
    application_list = Application.objects.filter(status=Application.Status.PENDING)
    return api_response(ErrorCode.SUCCESS,
                        data=ApplicationSimpleSerializer(application_list, many=True).data)


# 获取指定认领申请
@api_view(['GET'])
@login_required
def get_specified_application(request):
    application_id = request.GET.get('id')
    application = Application.objects.filter(id=application_id).first()
    if application is None:
        return api_response(ErrorCode.APPLICATION_NOT_FOUND)
    return api_response(ErrorCode.SUCCESS,
                        data=ApplicationDetailedSerializer(application).data)


def check_opinion(opinion: str):
    return opinion == 1 or \
        opinion.lower() == 'true' or \
        opinion.lower() == 'agree' or \
        opinion.lower() == 'pass'


# 审核门户申请
@api_view(['PUT'])
@login_required
def update_application_status(request):
    application_id = request.data.get('application_id')
    opinion = request.data.get('opinion')
    application = Application.objects.filter(id=application_id).first()
    if application is None:
        return api_response(ErrorCode.APPLICATION_NOT_FOUND)

    if check_opinion(opinion):
        application.status = Application.Status.PASSED
    else:
        application.status = Application.Status.FAILED
    application.save()
    create_message(application.id)
    return api_response(ErrorCode.SUCCESS)

def create_message(application_id):
    application = Application.objects.get(id=application_id)
    if application.status == Application.Status.PASSED:
        message = Message.objects.create(
            user=application.user,
            link_content=application.research_name,
            link_id=application.research_id
        )
        profile = UserProfile.objects.get(user=application.user)
        profile.researcher_id=application.research_id
        profile.save()
    else:
        message = Message.objects.create(
            user=application.user,
            research_id=-2,
            link_content=application.research_name,
            link_id=application.research_id
        )