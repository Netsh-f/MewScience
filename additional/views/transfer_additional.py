# ------- Litang Save The World! -------
#
# @Time    : 2023/12/24 13:11
# @Author  : Lynx
# @File    : transfer_additional.py
#
from django.contrib.auth.models import User
from rest_framework.decorators import api_view

from account.models import UserProfile
from additional.models import Patent, Project, Reward
from message.models import Message
from utils.error_code import ErrorCode
from utils.login_check import login_required
from utils.response_util import api_response


def get_portal_by_user(user: User):
    profile = UserProfile.objects.get(user=user)
    return profile.researcher_id

def get_user_by_portal(researcher_id):
    profile = UserProfile.objects.filter(researcher_id=researcher_id).first()
    if profile is None: return None
    else: return profile.user

@api_view(['PUT'])
@login_required
def transfer_patent(request):
    from_id = get_portal_by_user(request.user)
    patent_id = request.data.get('patent_id')
    to_id = request.data.get('transferee')
    if patent_id is None or to_id is None:
        return api_response(ErrorCode.INVALID_DATA)
    user = get_user_by_portal(to_id)
    if user is None:
        return api_response(ErrorCode.TRANSFEREE_NOT_REGISTERED)
    try:
        patent = Patent.objects.get(id=patent_id)
    except:
        return api_response(ErrorCode.PATENT_NOT_FOUND)

    Message.objects.create(user=user,
                           research_id=from_id,
                           link_content=patent.title,
                           link_id=patent_id,
                           msg_type=Message.MsgType.WORKS_TRANSFER,
                           work_type=Message.WorkType.PATENT)
    return api_response(ErrorCode.SUCCESS)

@api_view(['PUT'])
@login_required
def transfer_project(request):
    from_id = get_portal_by_user(request.user)
    project_id = request.data.get('project_id')
    to_id = request.data.get('transferee')
    if project_id is None or to_id is None:
        return api_response(ErrorCode.INVALID_DATA)
    user = get_user_by_portal(to_id)
    if user is None:
        return api_response(ErrorCode.TRANSFEREE_NOT_REGISTERED)
    try:
        project = Project.objects.get(id=project_id)
    except:
        return api_response(ErrorCode.PROJECT_NOT_FOUND)

    Message.objects.create(user=user,
                           research_id=from_id,
                           link_content=project.title,
                           link_id=project_id,
                           type=Message.MsgType.WORKS_TRANSFER,
                           work_type=Message.WorkType.PROJECT)
    return api_response(ErrorCode.SUCCESS)

@api_view(['PUT'])
@login_required
def transfer_reward(request):
    from_id = get_portal_by_user(request.user)
    reward_id = request.data.get('reward_id')
    to_id = request.data.get('transferee')
    if reward_id is None or to_id is None:
        return api_response(ErrorCode.INVALID_DATA)
    user = get_user_by_portal(to_id)
    if user is None:
        return api_response(ErrorCode.TRANSFEREE_NOT_REGISTERED)
    try:
        reward = Reward.objects.get(id=reward_id)
    except:
        return api_response(ErrorCode.REWARD_NOT_FOUND)

    Message.objects.create(user=user,
                           research_id=from_id,
                           link_content=reward.title,
                           link_id=reward_id,
                           type=Message.MsgType.WORKS_TRANSFER,
                           work_type=Message.WorkType.REWARD)
    return api_response(ErrorCode.SUCCESS)

@api_view(['PUT'])
@login_required
def process_patent_tran(request):
    opinion = request.data.get('opinion')
    patent_id = request.data.get('patent_id')
    if opinion is None or patent_id is None:
        return api_response(ErrorCode.INVALID_DATA)

    try:
        patent = Patent.objects.get(id=patent_id)
    except:
        return api_response(ErrorCode.PATENT_NOT_FOUND)

    portal = get_portal_by_user(request.user)
    if portal is None:
        return api_response()
