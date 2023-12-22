# ------- Litang Save The World! -------
#
# @Time    : 2023/12/22 11:08
# @Author  : Lynx
# @File    : urls.py
#

from django.urls import path

from message.views import get_msg_list

urlpatterns = [
    path('messages/list', get_msg_list),
]