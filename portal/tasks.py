# ------- Litang Save The World! -------
#
# @Time    : 2023/12/22 19:55
# @Author  : Lynx
# @File    : tasks.py
#
from celery import shared_task

from account.models import UserProfile
from message.models import Message
from portal.models import Application

# 异步添加信息
@shared_task
def create_message(application_id):
    application = Application.objects.get(id=application_id)
    if application.status == Application.Status.PASSED:
        message = Message.objects.create(
            user=application.user,
            research_name=application.research_name,
        )
        profile = UserProfile.objects.get(user=application.user)
        profile.researcher_id=application.research_id
    else:
        message = Message.objects.create(
            user=application.user,
            research_name=application.research_name,
            research_id=-2
        )