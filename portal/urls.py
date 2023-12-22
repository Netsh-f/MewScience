# ------- Litang Save The World! -------
#
# @Time    : 2023/12/19 20:49
# @Author  : Lynx
# @File    : urls.py
#
from django.urls import path
from views import claim_portal_view, get_applications_list, update_application_status

urlpatterns = [
    path('claim', claim_portal_view),
    path('applications/list', get_applications_list),
    path('applications/update', update_application_status)
]
