# ------- Litang Save The World! -------
#
# @Time    : 2023/12/19 20:49
# @Author  : Lynx
# @File    : urls.py
#
from django.urls import path

from portal.views import claim_portal, \
    get_applications_list, update_application_status, \
    get_specified_application

urlpatterns = [
    path('claim', claim_portal),
    path('applications/list', get_applications_list),
    path('applications/get', get_specified_application),
    path('applications/update', update_application_status)
]
