# ------- Litang Save The World! -------
#
# @Time    : 2023/12/19 20:49
# @Author  : Lynx
# @File    : urls.py
#
from django.urls import path

from portal import views

urlpatterns = [
    path('claim', views.claim_portal),
    path('applications/list', views.get_applications_list),
    path('applications/get', views.get_specified_application),
    path('applications/update', views.update_application_status),
    path('follow', views.follow_portal),
    path('unfollow', views.unfollow_portal),
]
