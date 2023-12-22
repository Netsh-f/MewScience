import os

from rest_framework.decorators import api_view
from celery import shared_task

from MewScience import settings
from account.models import UserProfile
from portal.models import Application
from portal.serializers import ApplicationSerializer
from utils.error_code import ErrorCode
from utils.file_check import file_check
from utils.response_util import api_response
from message.models import Message

# 申请认领门户
@api_view(['POST'])
def claim_portal_view(request):
    if request.user.is_authenticated:
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
            Application.objects.create(user=user, research_id=research_id, message=message, file=file_url)
            return api_response(ErrorCode.SUCCESS)
        else:
            return api_response(ErrorCode.INVALID_DATA)
    else:
        return api_response(ErrorCode.NOT_LOGGED_IN)

# 获取门户列表
@api_view(['GET'])
def get_applications_list(request):
    if request.user.is_authenticated:
        application_list = Application.objects.filter(status=Application.Status.PENDING)
        return api_response(ErrorCode.SUCCESS,
                            data=ApplicationSerializer(application_list, many=True).data)
    else:
        return api_response(ErrorCode.NOT_LOGGED_IN)

def check_opinion(opinion):
    return opinion is '1' or \
        opinion is 'true' or \
        opinion is 'True' or \
        opinion is 'agree'


# 审核门户申请
@api_view(['PUT'])
def update_application_status(request):
    if request.user.is_authenticated:
        application_id = request.data.get('application_id')
        opinion = request.data.get('opinion')
        application = Application.objects.get(id=application_id)
        if check_opinion(opinion):
            application.status = Application.Status.PASSED
        else:
            application.status = Application.Status.FAILED
        application.save()
        create_message.delay(application.id)
        return api_response(ErrorCode.SUCCESS)
    else:
        return api_response(ErrorCode.NOT_LOGGED_IN)

# 异步添加信息
@shared_task
def create_message(application_id):
    application = Application.objects.get(id=application_id)
    if application.Status == Application.Status.PASSED:
        message = Message.objects.create(
            content="您关于门户 的申请已通过！",
            user=application.user,
        )
    else:
        message = Message.objects.create(
            content="您关于门户 的申请未通过，请联系管理员获取详细信息！",
            user=application.user
        )
