# ------- Litang Save The World! -------
#
# @Time    : 2023/12/22 11:08
# @Author  : Lynx
# @File    : urls.py
#

from django.urls import path

from message import views

urlpatterns = [
    path('messages/list', views.get_msg_list),
    path('messages/update-status', views.update_message_status)
]